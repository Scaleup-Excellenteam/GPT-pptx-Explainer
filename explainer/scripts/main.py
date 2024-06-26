import argparse
import time
import asyncio
import os
from explainer.scripts.pptx_extractor import extract_text_from_presentation, text_to_json_file
from explainer.scripts.async_tasks import process_presentation
from explainer.scripts.ai_api import load_api_key
import logging
from logging.handlers import TimedRotatingFileHandler

# Base path to the project root
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print(f"Base path: {base_path}")

UPLOADS_FOLDER = os.path.join(base_path, "explainer/", "uploads")
OUTPUTS_FOLDER = os.path.join(base_path, "explainer/", "outputs")
LOGS_FOLDER = os.path.join(base_path, "explainer/", "logs")

os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(OUTPUTS_FOLDER, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)

log_handler = TimedRotatingFileHandler(os.path.join(LOGS_FOLDER, 'explainer.log'), when="midnight", interval=1, backupCount=5)
log_handler.suffix = "%Y-%m-%d"
log_handler.setLevel(logging.INFO)
logger = logging.getLogger('ExplainerLogger')
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

def get_key():
    api_key = load_api_key()
    if not api_key:
        logger.error("Error: The OpenAI API key is not set in the environment variables.")
        exit(1)
    logger.info("Loaded OpenAI API key from environment.")
    return api_key

def get_unprocessed_files():
    logger.info(f"Checking for unprocessed files in {UPLOADS_FOLDER}.")
    processed_files = {file.split(".")[0] for file in os.listdir(OUTPUTS_FOLDER)}
    all_files = {file.split(".")[0] for file in os.listdir(UPLOADS_FOLDER)}
    return all_files - processed_files

def runnig():
    print(f'get directory: {os.getcwd()}')
    api_key = get_key()
    while True:
        unprocessed = get_unprocessed_files()
        if not unprocessed:
            logger.info("No unprocessed files found. Sleeping for 10 seconds.")
            time.sleep(10)
            continue
        for file in unprocessed:
            presentation_path = os.path.join(UPLOADS_FOLDER, file + ".pptx")
            try:
                slides_text = extract_text_from_presentation(presentation_path)
                summaries = asyncio.run(process_presentation(slides_text, api_key))
                text_to_json_file(summaries, presentation_path, OUTPUTS_FOLDER)
                logger.info(f"Summarization completed for {file}.")
            except Exception as e:
                logger.error(f"Error processing file {file}: {e}")
        time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description="Extract text from a PowerPoint presentation and summarize it")
    parser.add_argument("presentation_path", type=str, nargs="?", help="Relative path to the PowerPoint presentation file.")
    args = parser.parse_args()

    presentation_path = args.presentation_path
    if not presentation_path:
        runnig()
        
    logger.info(f"Relative presentation path: {presentation_path}")
    
    if not os.path.isfile(presentation_path):
        logger.error(f"Error: The presentation file '{presentation_path}' does not exist.")
        exit(1)

    api_key = get_key()

    try:
        slides_text = extract_text_from_presentation(presentation_path)
        summaries = asyncio.run(process_presentation(slides_text, api_key))
        text_to_json_file(summaries, presentation_path, OUTPUTS_FOLDER)
        logger.info("Summarization completed and saved to JSON file.")
    except Exception as e:
        logger.error(f"Error processing file {presentation_path}: {e}")

if __name__ == "__main__":
    main()
