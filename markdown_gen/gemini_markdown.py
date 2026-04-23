import asyncio
import os
import time
import json
import traceback
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# Third-party imports
from dotenv import load_dotenv
from tqdm.asyncio import tqdm
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuration matching Script B's concurrency style
MAX_CONCURRENCY = 5
MAX_RETRIES = 3  # Number of retry attempts
RETRY_DELAY = 2  # Seconds to wait between retries

SCRIPT_DIR = Path(__file__).parent
INPUT_DIR = Path("PDFs")
BASE_OUTPUT_DIR = Path("gemini_results")
MARKDOWNS_DIR = BASE_OUTPUT_DIR / "markdowns"
JSONL_OUTPUT = BASE_OUTPUT_DIR / "results.jsonl"

with open(SCRIPT_DIR / "ai_prompt.md", "r") as f:
    MASTER_PROMPT = f.read()

# Model Selection
MODEL_ID = "gemini-3-pro-preview"

PRICING_REGISTRY = {
    "gemini-1.5-flash": {
        "input_low": 0.075,   "input_high": 0.15,
        "output_low": 0.30,   "output_high": 0.60,
        "tier_cutoff": 128_000
    },
    "gemini-1.5-pro": {
        "input_low": 1.25,    "input_high": 2.50,
        "output_low": 5.00,   "output_high": 10.00,
        "tier_cutoff": 128_000
    },
    "gemini-2.0-flash": {
        "input_low": 0.10,    "input_high": 0.10,
        "output_low": 0.40,   "output_high": 0.40,
        "tier_cutoff": float('inf')
    },
    "gemini-3-pro-preview": {
        "input_low": 2.00,    "input_high": 4.00,
        "output_low": 12.00,  "output_high": 18.00,
        "tier_cutoff": 200_000
    }
}

# -----------------------------------------------------------------------------
# Helpers: Cost & Sync Logic
# -----------------------------------------------------------------------------

def calculate_cost(model_id: str, input_tok: int, output_tok: int) -> float:
    """Calculates cost based on Script A's pricing registry."""
    base_model = next((k for k in PRICING_REGISTRY if k in model_id), None)
    if not base_model:
        return 0.0

    pricing = PRICING_REGISTRY[base_model]
    total_context = input_tok + output_tok
    
    if total_context <= pricing["tier_cutoff"]:
        rate_in, rate_out = pricing["input_low"], pricing["output_low"]
    else:
        rate_in, rate_out = pricing["input_high"], pricing["output_high"]
        
    cost = (input_tok / 1_000_000 * rate_in) + (output_tok / 1_000_000 * rate_out)
    return round(cost, 6)

def _sync_gemini_transaction(client: genai.Client, pdf_path: Path, model: str) -> Dict[str, Any]:
    """
    Executes the blocking Google GenAI transaction (Upload -> Poll -> Generate -> Delete).
    This logic is taken directly from Script A but returns a dict instead of logging.
    """
    filename = pdf_path.name
    start_time = time.time()
    uploaded_file = None
    
    result_data = {
        "status": "FAILURE",
        "markdown": None,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost": 0.0,
        "duration_seconds": 0,
        "error_msg": None
    }

    try:
        # 1. Upload
        uploaded_file = client.files.upload(
            file=pdf_path,
            config=types.UploadFileConfig(display_name=filename)
        )

        # 2. Poll
        while uploaded_file.state == "PROCESSING":
            time.sleep(1)
            uploaded_file = client.files.get(name=uploaded_file.name)
        
        if uploaded_file.state != "ACTIVE":
            raise RuntimeError(f"File state: {uploaded_file.state}")

        # 3. Generate
        prompt_text = MASTER_PROMPT
        response = client.models.generate_content(
            model=model,
            contents=[prompt_text, uploaded_file],
        )

        # 4. Metrics
        if response.usage_metadata:
            in_tok = response.usage_metadata.prompt_token_count
            out_tok = response.usage_metadata.candidates_token_count
            result_data["input_tokens"] = in_tok
            result_data["output_tokens"] = out_tok
            result_data["cost"] = calculate_cost(model, in_tok, out_tok)

        result_data["markdown"] = response.text if response.text else ""
        
        # Validation
        finish_reason = "UNKNOWN"
        if response.candidates:
            finish_reason = str(response.candidates[0].finish_reason)
            
        if finish_reason != "FinishReason.STOP":
            print(finish_reason)
            raise ValueError(f"Abnormal finish: {finish_reason}")
        if not result_data["markdown"].strip():
            raise ValueError("Empty output from model")

        result_data["status"] = "SUCCESS"

    except Exception as e:
        result_data["error_msg"] = str(e)
        # result_data["traceback"] = traceback.format_exc() # Uncomment for deep debug
    
    finally:
        # 5. Cleanup
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name)
            except Exception:
                pass # Fail silently on cleanup
        
        result_data["duration_seconds"] = round(time.time() - start_time, 2)

    return result_data

# -----------------------------------------------------------------------------
# Async Pipeline with Retry Logic
# -----------------------------------------------------------------------------

async def append_jsonl(record: dict):
    """Append a single JSON record to the JSONL file."""
    with JSONL_OUTPUT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

async def parse_document(client: genai.Client, path: Path, sem: asyncio.Semaphore) -> tuple[Path, bool]:
    """
    Wraps the sync Gemini transaction in a thread with retry logic.
    """
    async with sem:
        timestamp = datetime.now(timezone.utc)
        result = None
        all_errors = []
        
        # Retry loop
        for attempt in range(1, MAX_RETRIES + 1):
            # Run blocking GenAI logic in a thread
            result = await asyncio.to_thread(_sync_gemini_transaction, client, path, MODEL_ID)
            
            if result["status"] == "SUCCESS":
                break  # Success, exit retry loop
            
            # Failed attempt
            all_errors.append(f"Attempt {attempt}: {result['error_msg']}")
            
            if attempt < MAX_RETRIES:
                # Wait before retrying
                await asyncio.sleep(RETRY_DELAY * attempt)  # Exponential backoff
            else:
                # Final attempt failed
                result["error_msg"] = " | ".join(all_errors)

        if result["status"] == "SUCCESS":
            # ---------- SAVE MARKDOWN FILE ----------
            md_filename = f"{path.stem}.md"
            md_path = MARKDOWNS_DIR / md_filename
            
            md_path.write_text(result["markdown"], encoding="utf-8")

            # ---------- JSONL RECORD ----------
            record = {
                "timestamp": timestamp.isoformat(),
                "file": str(path),
                "model": MODEL_ID,
                "status": "SUCCESS",
                "duration_seconds": result["duration_seconds"],
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "estimated_cost_usd": result["cost"],
                "markdown_file": str(md_path),
                "attempts": attempt
            }
            
            await append_jsonl(record)
            return path, True

        else:
            # ---------- FAILURE RECORD ----------
            record = {
                "timestamp": timestamp.isoformat(),
                "file": str(path),
                "model": MODEL_ID,
                "status": "FAILURE",
                "error": result["error_msg"],
                "duration_seconds": result["duration_seconds"],
                "attempts": MAX_RETRIES
            }
            await append_jsonl(record)
            return path, False

async def main():
    # 0. Check API Key
    if not GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        return

    # 1. Create directories
    BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MARKDOWNS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. Check Inputs
    if not INPUT_DIR.exists():
        print(f"❌ Error: Input directory '{INPUT_DIR}' not found.")
        return
        
    # Get all PDFs
    all_pdfs = list(INPUT_DIR.glob("*.pdf"))
    files_to_parse = [f for f in all_pdfs if not (MARKDOWNS_DIR / f.with_suffix('.md').name).exists()]

    # Only process PDFs that are missing their .md output
    
    # If you want to filter specific files, uncomment and modify:
    # SPECIFIC_FILES = ["file1.pdf", "file2.pdf"]
    # files_to_parse = [f for f in files_to_parse if f.name in SPECIFIC_FILES]
    
    if not files_to_parse:
        if not all_pdfs:
            print(f"❌ No PDFs found in '{INPUT_DIR}'.")
        else:
            print(f"✅ All {len(all_pdfs)} PDFs have already been processed. Nothing to do.")
        return

    print(f"🔄 Will retry failed documents up to {MAX_RETRIES} times\n")

    # 3. Initialize Client & Semaphore
    client = genai.Client(api_key=GOOGLE_API_KEY)
    sem = asyncio.Semaphore(MAX_CONCURRENCY)

    # 4. Run and gather results
    results = await tqdm.gather(
        *[parse_document(client, path, sem) for path in files_to_parse],
        desc=f"Processing PDFs with {MODEL_ID}"
    )

    # 5. Analyze failures
    failed_files = [path.name for path, success in results if not success]
    
    # 6. Print Summary
    print("\n" + "="*40)
    print(f"PROCESSING COMPLETE")
    print("="*40)
    print(f"Total Files: {len(files_to_parse)}")
    print(f"Successful:  {len(files_to_parse) - len(failed_files)}")
    print(f"Failed:      {len(failed_files)}")
    
    if failed_files:
        print("\nFiles that failed (after all retries):")
        print("-" * 40)
        for fname in failed_files:
            print(f"❌ {fname}")
    else:
        print("\n✅ All files processed successfully.")
    print("="*40 + "\n")
    print(f"Results log: {JSONL_OUTPUT}")
    print(f"Markdowns:   {MARKDOWNS_DIR}")

if __name__ == "__main__":
    asyncio.run(main())