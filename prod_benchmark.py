"""
PDF Processing and Benchmarking Pipeline.

This module provides a pipeline for extracting annotations from PDFs,
combining them with OCR text, cleaning the text, and benchmarking
various markdown conversion methods against ground truth data.
"""

import argparse
import json
import logging
import os
import re
from collections import defaultdict

import pandas as pd
import pymupdf
from cleantext import clean

from benchmark_data.utils import find_best_match_and_normalized_distance


# ==============================================================================
# LOGGING SETUP
# ==============================================================================


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        verbose: If True, sets logging level to DEBUG; otherwise INFO.
        
    Returns:
        Configured logger instance.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


# ==============================================================================
# STEP 1: PDF ANNOTATION EXTRACTION
# ==============================================================================


def extract_highlighted_text(pdf_path: str, logger: logging.Logger) -> list[dict]:
    """
    Extract highlighted text from PDFs with annotations.

    Args:
        pdf_path: Path to a PDF file or directory containing PDFs.
        logger: Logger instance for output.

    Returns:
        List of annotation dictionaries containing page number, annotation key/text, and source.
    """
    logger.info(f"Starting PDF annotation extraction from: {pdf_path}")
    
    # Get list of PDF files
    if os.path.isdir(pdf_path):
        pdf_files = sorted(
            [os.path.join(pdf_path, f) for f in os.listdir(pdf_path) if f.lower().endswith(".pdf")],
            key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[-1])
            if "_" in os.path.basename(x) else x
        )
    else:
        pdf_files = [pdf_path]
    
    logger.info(f"Found {len(pdf_files)} PDF(s) to process")
    json_output = []
    
    for idx, file_path in enumerate(pdf_files, start=1):
        logger.info(f"Processing PDF {idx}/{len(pdf_files)}: {file_path}")
        doc = pymupdf.open(file_path)
        page = doc[0]
        
        # Find source annotation for this page
        page_source = ""
        for annot in page.annots():
            content = annot.info.get('content', '').strip()
            if 'source' in content.lower():
                page_source = content
                break
        
        # Process highlight annotations
        for annot in page.annots():
            content = annot.info.get('content', '').strip()
            
            # Skip source annotations
            if 'source' in content.lower():
                continue
            
            # Check for pattern (1.1, 1.2, etc.) and highlight type
            match = re.match(r'^(\d+\.\d+)', content)
            if match and annot.type[1] == 'Highlight':  # Highlight annotation
                key = match.group(1)
                
                # Extract text within the annotation rectangle
                final_text = page.get_text("text", clip=annot.rect, sort=True).strip()

                # Clean the extracted text
                final_text = ' '.join(final_text.split())  # Remove \n and extra spaces
                
                if final_text:
                    json_output.append({
                        'page_number': idx,
                        'annotation': {
                            'key': key,
                            'text': final_text
                        },
                        'source': page_source
                    })
        
        doc.close()
    
    # Sort by page and annotation key
    json_output.sort(key=lambda x: (x['page_number'], float(x['annotation']['key'])))
    logger.info(f"Extracted {len(json_output)} annotations")
    
    return json_output


# ==============================================================================
# STEP 2: COMBINE ANNOTATIONS WITH OCR
# ==============================================================================

def parse_key(key: str) -> tuple[int, int]:
    """Parse annotation key (e.g., '1.1' -> (1, 1))."""
    parts = key.split(".")
    return (int(parts[0]), int(parts[1]))


def combine_annotations_with_ocr(
    annotations: list[dict], excel_path: str, logger: logging.Logger
) -> list[dict]:
    """
    Combine annotations with OCR text from Excel.

    Args:
        annotations: List of annotation dictionaries from extract_highlighted_text.
        excel_path: Path to Excel file containing OCR text data.
        logger: Logger instance for output.

    Returns:
        List of dictionaries with combined annotation and OCR data per page.
    """
    logger.info("Combining annotations with OCR text")
    
    # Read Excel file
    df = pd.read_excel(excel_path)
    logger.info(f"Loaded {len(df)} OCR entries from Excel")
    
    # Group annotations by page
    annotations_by_page = defaultdict(lambda: defaultdict(list))
    
    for annotation in annotations:
        page_num = annotation['page_number']
        key = annotation['annotation']['key']
        text = annotation['annotation']['text']
        
        # Parse the key to get series and sequence
        series, sequence = parse_key(key)
        
        # Store with series as main grouping
        annotations_by_page[page_num][series].append({
            'sequence': sequence,
            'text': text
        })
    
    # Create the combined structure
    combined_data = {}
    
    # Process annotations
    for page_num, series_data in annotations_by_page.items():
        if page_num not in combined_data:
            combined_data[page_num] = {}
        
        # Sort and combine each series
        for series, texts in series_data.items():
            # Sort by sequence number
            sorted_texts = sorted(texts, key=lambda x: x['sequence'])
            
            # Combine texts in order
            combined_text = ' '.join([t['text'] for t in sorted_texts])
            
            # Store as separate reading order
            combined_data[page_num][f'series_{series}'] = combined_text
    
    # Add OCR text from dataframe
    for _, row in df.iterrows():
        page_num = row['Page No.']
        text = row['Text']
        
        if page_num not in combined_data:
            combined_data[page_num] = {}
        
        # Add OCR text to a separate array
        if 'text' not in combined_data[page_num]:
            combined_data[page_num]['text'] = []
        
        combined_data[page_num]['text'].append(text)
    
    # Convert to a more readable format
    final_output = []
    
    for page_num in sorted(combined_data.keys()):
        page_data = {
            'page_number': page_num,
            'annotations': {},
            'ocr_text': []
        }
        
        # Add annotation series
        for key, value in combined_data[page_num].items():
            if key.startswith('series_'):
                series_num = key.replace('series_', '')
                page_data['annotations'][f'reading_order_{series_num}'] = value
            elif key == 'text':
                page_data['ocr_text'] = value
        
        final_output.append(page_data)
    
    logger.info(f"Combined data for {len(final_output)} pages")
    return final_output


# ==============================================================================
# STEP 3: TEXT CLEANING
# ==============================================================================

def extract_and_clean_by_page(
    data: list[dict], logger: logging.Logger
) -> list[dict]:
    """
    Extract and clean text, grouped by page number.

    Processes both annotations and OCR text, returning cleaned text with OCR flags.

    Args:
        data: Combined annotation and OCR data from combine_annotations_with_ocr.
        logger: Logger instance for output.

    Returns:
        List of dictionaries with page_number, texts array, and is_ocr flags.
    """
    logger.info("Cleaning and processing text")
    result = []
    
    for item in data:
        # Skip items without page numbers
        if 'page_number' not in item:
            continue
            
        page_number = item['page_number']
        cleaned_texts = []
        is_ocr_flags = []
        
        # Extract and clean annotation texts (sorted by reading order)
        if 'annotations' in item:
            annotations = item['annotations']
            annotation_pairs = []
            
            for key, text in annotations.items():
                if key.startswith('reading_order_') and isinstance(text, str):
                    # Extract the order number for sorting
                    try:
                        order_num = int(key.split('_')[2])
                    except (IndexError, ValueError):
                        order_num = 0

                    # NOTE: We intentionally skip autocorrect and aggressive cleaning here.
                    # Autocorrect can cause false positives (e.g., "field" -> "fiend").
                    # Aggressive cleaning replaces foreign language characters with English equivalents.
                    cleaned_text = text

                    if cleaned_text.strip():
                        annotation_pairs.append((order_num, cleaned_text.strip()))
            
            # Sort annotations by reading order and add to cleaned_texts
            annotation_pairs.sort(key=lambda x: x[0])
            for _, text in annotation_pairs:
                cleaned_texts.append(text)
                is_ocr_flags.append(False)  # Annotation text, not OCR
        
        # Extract and clean OCR texts
        if 'ocr_text' in item and isinstance(item['ocr_text'], list):
            for ocr_text in item['ocr_text']:
                if isinstance(ocr_text, str) and ocr_text.strip():
                    # Clean the OCR text
                    cleaned_ocr = clean(
                        ocr_text,
                        lower=False,
                        normalize_whitespace=True,
                        fix_unicode=False,
                        strip_lines=True,
                        no_line_breaks=True,
                        lang="en"
                    )
                    
                    if cleaned_ocr.strip():
                        cleaned_texts.append(cleaned_ocr.strip())
                        is_ocr_flags.append(True)  # OCR text
        
        # Only add pages that have text content
        if cleaned_texts:
            result.append({
                'page_number': page_number,
                'texts': cleaned_texts,
                'is_ocr': is_ocr_flags
            })
    
    logger.info(f"Cleaned {len(result)} pages")
    return result


# ==============================================================================
# STEP 4: BENCHMARKING
# ==============================================================================

def generate_raw_scores(
    ground_truth_data: list[dict],
    folder_info: list[tuple[str, str]],
    logger: logging.Logger,
) -> pd.DataFrame:
    """
    Process ground truth data against markdown files from various methods.

    For each piece of text ("needle") in the ground truth, this function searches
    for the best match in the corresponding page's markdown file ("haystack")
    for each specified method.

    Args:
        ground_truth_data: List of dictionaries, each containing 'page_number'
            and a list of 'texts' to find.
        folder_info: List of tuples (folder_path, column_name) defining each
            method's markdown folder and the desired score column name.
        logger: Logger instance for output.

    Returns:
        DataFrame containing the raw scores (normalized distances)
        for each needle against each method, including OCR flag.
    """
    all_results = []
    total_entries = len(ground_truth_data)

    logger.info("Generating raw scores...")
    for index, ground_truth_entry in enumerate(ground_truth_data):
        logger.info(f"Processing page group {index + 1}/{total_entries}")
        page_number = ground_truth_entry['page_number']
        is_ocr_list = ground_truth_entry.get('is_ocr', [])

        for needle_index, needle_text in enumerate(ground_truth_entry['texts']):
            row = {
                'page_number': page_number,
                'needle_index': needle_index,
                'needle': needle_text,
                'OCR': is_ocr_list[needle_index] if needle_index < len(is_ocr_list) else False
            }

            for folder_name, col_name in folder_info:
                markdown_path = f"{folder_name}/page_{page_number}.md"
                try:
                    with open(markdown_path, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                    
                    # The score is the normalized distance; lower is better.
                    best_match, score = find_best_match_and_normalized_distance(needle_text, md_content)
                except FileNotFoundError:
                    score = None
                    best_match = None
                
                row[col_name] = score
                row[f"{col_name}_best_match"] = best_match
            
            all_results.append(row)

    logger.info(f"Generated {len(all_results)} score entries")
    return pd.DataFrame(all_results)


def analyze_results(
    scores_df: pd.DataFrame,
    mapping_file: str,
    score_columns: list[str],
    min_score_threshold: float,
    excluded_folders: list[str],
    logger: logging.Logger,
) -> pd.DataFrame:
    """
    Analyze raw scores to produce a final summary report.

    This function merges scores with page-folder mappings, filters data,
    calculates mean accuracy, adds folder counts, computes a weighted
    average, and sorts the results for presentation.

    Args:
        scores_df: DataFrame with raw scores from generate_raw_scores.
        mapping_file: Path to the CSV file mapping page numbers to folders.
        score_columns: List of column names containing scores.
        min_score_threshold: Threshold for filtering results.
        excluded_folders: List of folders to exclude from analysis.
        logger: Logger instance for output.

    Returns:
        DataFrame containing the final, formatted benchmark results.
    """
    logger.info("Analyzing results...")

    # 1. Merge with page-folder mapping
    page_mapping_df = pd.read_csv(mapping_file)
    merged_df = scores_df.merge(page_mapping_df, left_on="page_number", right_on="Page")

    # 2. Filter data
    # Drop rows where any method failed to produce a score
    filtered_df = merged_df.dropna(subset=score_columns).copy()

    # Exclude specified folders (e.g., 'test' folders)
    filtered_df = filtered_df[~filtered_df["Folder"].isin(excluded_folders)]
    # Keep only rows where at least one method found a close match
    filtered_df = filtered_df[filtered_df[score_columns].min(axis=1) < min_score_threshold]
    filtered_df.to_csv("benchmark_granular.csv", index=False)

    if filtered_df.empty:
        logger.warning("No data left after filtering. Cannot generate report.")
        return pd.DataFrame()

    # 3. Calculate mean scores (distances) grouped by folder type
    mean_distances = filtered_df.groupby("Folder")[score_columns].mean()

    # 4. Convert distance to accuracy percentage and add folder counts
    # Accuracy = (1 - distance) * 100
    final_report = ((1 - mean_distances) * 100).round(2)
    folder_counts = filtered_df.groupby("Folder").size()
    final_report['Folder_Count'] = folder_counts.astype(int)

    # 5. Calculate and append a weighted mean row
    total_count = folder_counts.sum()
    weighted_means = {}
    for col in score_columns:
        weighted_mean_distance = (mean_distances[col] * folder_counts).sum() / total_count
        weighted_mean_accuracy = ((1 - weighted_mean_distance) * 100).round(2)
        weighted_means[col] = weighted_mean_accuracy
        
    weighted_mean_row = pd.Series(weighted_means, name='Weighted_Mean')
    weighted_mean_row['Folder_Count'] = int(total_count)
    final_report = pd.concat([final_report, weighted_mean_row.to_frame().T])

    # 6. Sort columns by performance (descending weighted mean accuracy)
    weighted_accuracies = final_report.loc['Weighted_Mean', score_columns]
    sorted_cols = weighted_accuracies.sort_values(ascending=False).index.tolist()
    final_report = final_report[sorted_cols + ['Folder_Count']]

    logger.info("Analysis complete")
    return final_report


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def main() -> int:
    """
    Run the entire PDF processing and benchmarking pipeline.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='PDF Processing and Benchmarking Pipeline',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input files
    parser.add_argument('--pdf-path', type=str, default='PDFs/',
                        help='Path to PDF file or directory containing PDFs')
    parser.add_argument('--excel-path', type=str, default='benchmark_data/Pictures.xlsx',
                        help='Path to Excel file with OCR text')
    parser.add_argument('--page-mapping', type=str, default='benchmark_data/page_folder_mapping.csv',
                        help='Path to page-folder mapping CSV file')
    
    # Output files
    parser.add_argument('--annotations-output', type=str, default='benchmark_data/annotations.json',
                        help='Output path for extracted annotations')
    parser.add_argument('--combined-output', type=str, default='benchmark_data/combined_output.json',
                        help='Output path for combined data')
    parser.add_argument('--cleaned-output', type=str, default='benchmark_data/cleaned_output.json',
                        help='Output path for cleaned data')
    parser.add_argument('--benchmark-output', type=str, default='benchmark_results_final.csv',
                        help='Output path for benchmark results')
    
    # Benchmark configuration
    parser.add_argument('--min-score-threshold', type=float, default=0.25,
                        help='Minimum score threshold for benchmark filtering')
    parser.add_argument('--excluded-folders', type=str, nargs='+', default=['test'],
                        help='Folders to exclude from benchmark analysis')
    
    # Logging
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    logger.info("="*70)
    logger.info("PDF PROCESSING AND BENCHMARKING PIPELINE")
    logger.info("="*70)
    
    # Define folder info for benchmarking
    folder_info = [
        ('reducto_results/markdowns', 'reducto'),
        ('datalab_results/markdowns', 'datalab'),
        ('gemini_results/markdowns', 'gemini'),
        ('llama_parse_results/markdowns', 'llama_parse'),
        ('pymupdflayout_results/markdowns', 'pymupdflayout'),
        ('docling_wocr_results/markdowns', 'docling_cpu_without_ocr'),
        ('docling_ocr_results/markdowns', 'docling_cpu_with_ocr'),
    ]
    score_columns = [col_name for _, col_name in folder_info]
    
    try:
        # STEP 1: Extract PDF annotations
        logger.info("\n" + "="*70)
        logger.info("STEP 1: Extracting PDF annotations")
        logger.info("="*70)
        annotations = extract_highlighted_text(args.pdf_path, logger)
        
        # Save intermediate result
        with open(args.annotations_output, 'w', encoding='utf-8') as f:
            json.dump(annotations, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved annotations to: {args.annotations_output}")
        
        # STEP 2: Combine with OCR text
        logger.info("\n" + "="*70)
        logger.info("STEP 2: Combining annotations with OCR text")
        logger.info("="*70)
        combined_data = combine_annotations_with_ocr(annotations, args.excel_path, logger)
        
        # Save intermediate result
        with open(args.combined_output, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2)
        logger.info(f"Saved combined data to: {args.combined_output}")
        
        # STEP 3: Clean text
        logger.info("\n" + "="*70)
        logger.info("STEP 3: Cleaning text")
        logger.info("="*70)
        cleaned_data = extract_and_clean_by_page(combined_data, logger)
        
        # Save intermediate result
        with open(args.cleaned_output, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved cleaned data to: {args.cleaned_output}")
        
        # STEP 4: Run benchmarks
        logger.info("\n" + "="*70)
        logger.info("STEP 4: Running benchmarks")
        logger.info("="*70)
        raw_scores_df = generate_raw_scores(cleaned_data, folder_info, logger)

        final_results = analyze_results(
            raw_scores_df,
            args.page_mapping,
            score_columns,
            args.min_score_threshold,
            args.excluded_folders,
            logger
        )
        
        if not final_results.empty:
            final_results.to_csv(args.benchmark_output)
            logger.info(f"Saved benchmark results to: {args.benchmark_output}")
            logger.info("\nFinal Benchmark Results:")
            logger.info("\n" + str(final_results))
        
        # Pipeline complete
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*70)
        logger.info(f"Annotations: {args.annotations_output}")
        logger.info(f"Combined data: {args.combined_output}")
        logger.info(f"Cleaned data: {args.cleaned_output}")
        logger.info(f"Benchmark results: {args.benchmark_output}")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error during pipeline execution: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
