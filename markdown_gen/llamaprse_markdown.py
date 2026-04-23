import asyncio
from pathlib import Path
import json
from datetime import datetime, timezone
import os
import time

# Third-party imports
from dotenv import load_dotenv
from llama_cloud_services import LlamaParse


# Load environment variables
load_dotenv()
llama_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

# --- Configuration ---
INPUT_DIR = Path("PDFs")
NUM_WORKERS = 5
BASE_OUTPUT_DIR = Path("llama_parse_results")
MARKDOWNS_DIR = BASE_OUTPUT_DIR / "markdowns"
JSONL_OUTPUT = BASE_OUTPUT_DIR / "results.jsonl"

# --- Model & Cost Configuration ---
# 1. Define your models and their costs here
MODEL_COSTS = {
    "anthropic-sonnet-4.5": 90,
}

# 2. Select the model you want to use
SELECTED_MODEL = "anthropic-sonnet-4.5"

def get_parser():
    """
    Returns a configured LlamaParse instance using the SELECTED_MODEL.
    """
    print(f"ℹ️  Initializing parser with model: {SELECTED_MODEL}")
    return LlamaParse(
        api_key=llama_api_key,
        num_workers=NUM_WORKERS, 
        parse_mode="parse_page_with_agent",
        model=SELECTED_MODEL,  # Uses the variable defined above
        high_res_ocr=True, 
        adaptive_long_table=False,
        output_tables_as_HTML=False,
        precise_bounding_box=False,
        page_separator="\n\n---\n\n",
        verbose=False 
    )

def save_single_result(result, file_path):
    """
    Process and save a single result immediately.
    Returns (success: bool, record: dict)
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    original_path = Path(file_path)
    model_credit_cost = MODEL_COSTS.get(SELECTED_MODEL, 0)
    
    try:
        if result is None:
            raise ValueError("Received None result from parser")
        
        # Extract Markdown
        md_docs = result.get_markdown_documents(split_by_page=True)
        
        full_markdown = ""
        parsing_error = None
        
        if not md_docs:
            parsing_error = "No markdown documents extracted"
        else:
            full_markdown = "\n\n".join([doc.text for doc in md_docs])
            if not full_markdown.strip():
                parsing_error = "Extracted markdown is empty"

        # Save Markdown File
        md_filename = f"{original_path.stem}.md"
        md_path = MARKDOWNS_DIR / md_filename
        
        try:
            md_path.write_text(full_markdown, encoding="utf-8")
        except IOError as e:
            raise IOError(f"Failed to write markdown file: {e}")

        # Extract Metadata
        job_id = getattr(result, 'job_id', "N/A")
        credits_used = model_credit_cost
        
        if hasattr(result, 'pages') and result.pages:
            num_pages = len(result.pages)
        elif md_docs:
            num_pages = len(md_docs)
        else:
            num_pages = 0

        # Determine Status & Build Record
        if parsing_error:
            status = "failed"
            record_error = parsing_error
        else:
            status = "success"
            record_error = None

        record = {
            "timestamp": timestamp,
            "service": "llama-cloud",
            "model": SELECTED_MODEL,
            "file": str(original_path),
            "filename": original_path.name,
            "job_id": job_id,
            "markdown_file": str(md_path),
            "status": status,
            "credits_used": credits_used,
            "pages": num_pages
        }
        
        if record_error:
            record["error"] = record_error

        # Write to JSONL immediately
        try:
            with open(JSONL_OUTPUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except IOError as e:
            print(f"❌ Error writing JSONL: {e}")

        return (status == "success", record)

    except Exception as e:
        record = {
            "timestamp": timestamp,
            "file": str(original_path),
            "filename": original_path.name,
            "error": str(e),
            "status": "failed"
        }
        # Still try to write error to JSONL
        try:
            with open(JSONL_OUTPUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except IOError:
            pass
        return (False, record)


async def parse_single_file(parser, file_path, semaphore):
    """
    Parse a single file with semaphore-controlled concurrency.
    """
    async with semaphore:
        try:
            result = await parser.aparse(str(file_path))

            num_pages = len(result.pages) if hasattr(result, 'pages') and result.pages else 0

            return {
                "file_path": file_path,
                "status": "success",
                "result": result,
                "pages": num_pages,
            }
        except Exception as e:
            return {
                "file_path": file_path,
                "status": "error",
                "error": str(e),
            }


async def main():
    # 1. Validation
    if not llama_api_key:
        print("❌ Error: LLAMA_CLOUD_API_KEY not found in environment variables")
        return

    # Validate Dictionary Config
    if SELECTED_MODEL not in MODEL_COSTS:
        print(f"⚠️ Warning: Model '{SELECTED_MODEL}' not found in MODEL_COSTS dictionary.")
        print("   Credits will be recorded as 0.")
    
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ Error: No PDF files found in '{INPUT_DIR}'")
        return

    # 2. Setup
    try:
        BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        MARKDOWNS_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"❌ Error creating output directories: {e}")
        return
    
    # 3. Execution
    print(f"🚀 Starting LlamaParse Batch")
    print(f"🤖 Model: {SELECTED_MODEL}")
    print(f"💰 Cost per file: {MODEL_COSTS.get(SELECTED_MODEL, 'Unknown')}")
    print(f"📄 Files to Process: {len(pdf_files)}")
    print(f"⚙️  Max Concurrent Workers: {NUM_WORKERS}")
    
    # Initialize parser with num_workers=1 since we control concurrency with semaphore
    parser = LlamaParse(
        api_key=llama_api_key,
        num_workers=1,  # We control concurrency with semaphore
        parse_mode="parse_page_with_agent",
        model=SELECTED_MODEL,
        high_res_ocr=True, 
        adaptive_long_table=False,
        output_tables_as_HTML=False,
        precise_bounding_box=False,
        page_separator="\n\n---\n\n",
        verbose=False,
        show_progress=False,  # We'll show our own progress
    )
    
    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(NUM_WORKERS)
    
    start_time = time.time()
    
    # Create tasks for all files
    tasks = [
        asyncio.create_task(parse_single_file(parser, pdf_file, semaphore))
        for pdf_file in pdf_files
    ]
    
    # Process results as they complete and save immediately
    successfully_extracted_count = 0
    error_count = 0
    
    # Use tqdm with manual update for a single progress bar
    from tqdm import tqdm
    
    with tqdm(total=len(tasks), desc="Parsing PDFs", unit="file") as pbar:
        for coro in asyncio.as_completed(tasks):
            parse_result = await coro
            
            if parse_result["status"] == "success":
                # Eagerly save result to disk
                success, record = save_single_result(
                    parse_result["result"],
                    parse_result["file_path"]
                )
                if success:
                    successfully_extracted_count += 1
                else:
                    error_count += 1
            else:
                error_count += 1
                # Save error record
                save_single_result(None, parse_result["file_path"])
            
            pbar.update(1)

    duration = time.time() - start_time
    print(f"\n✅ Batch finished in {duration:.2f} seconds")

    # Summary Statistics
    cost_per_file = MODEL_COSTS.get(SELECTED_MODEL, 0)
    total_credits = len(pdf_files) * cost_per_file
    
    print(f"\n📊 Summary:")
    print(f"   Total Files Processed: {successfully_extracted_count}/{len(pdf_files)}")
    print(f"   Parse Errors: {error_count}")
    print(f"   Total Credits Used: {total_credits}")
    print(f"   (Based on fixed cost: {cost_per_file} credits/file for {SELECTED_MODEL})")
    
    print(f"\n🎯 Total files extracted correctly: {successfully_extracted_count}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")