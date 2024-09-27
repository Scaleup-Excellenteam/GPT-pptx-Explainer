import argparse
import time
import asyncio
import os
from explainer.scripts.pptx_extractor import extract_text_from_presentation, text_to_json_file
from explainer.scripts.async_tasks import process_presentation
from explainer.scripts.ai_api import load_api_key
import logging
from logging.handlers import TimedRotatingFileHandler
from configs import explainer_config as config

def setup_logger():
    log_handler = TimedRotatingFileHandler(config.LOG_FILE, when="midnight", interval=1, backupCount=5)
    log_handler.suffix = "%Y-%m-%d"
    log_handler.setLevel(logging.INFO)
    logger = logging.getLogger('ExplainerLogger')
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

def get_key() -> str:
    api_key = load_api_key()
    if not api_key:
        logger.error("Error: The OpenAI API key is not set in the environment variables.")
        exit(1)
    logger.info("Loaded OpenAI API key from environment.")
    return api_key

def get_unprocessed_files() -> set:
    logger.info(f"Checking for unprocessed files in {config.UPLOADS_FOLDER}.")
    processed_files = {file.split(".")[0] for file in os.listdir(config.OUTPUTS_FOLDER)}
    all_files = {file.split(".")[0] for file in os.listdir(config.UPLOADS_FOLDER)}
    return all_files - processed_files

def print_intro():
    intro_message = """
    \033[1;32m
    ***********************************************
    *                                             *
    *                  EXPLAINER                  *
    *                                             *
    ***********************************************
    * This is the main explainer script.          *
    * The interface with the project is done      *
    * through the client.                         *
    *                                             *
    * Usage:                                      *
    *   - Run this script to start the explainer  *
    *     process.                                *
    *                                             *
    ***********************************************
    \033[0m
    """
    print(intro_message)

def running() -> None:
    api_key = get_key()
    print_intro()
    while True:
        unprocessed = get_unprocessed_files()
        if not unprocessed:
            logger.info("No unprocessed files found. Sleeping for 10 seconds.")
            time.sleep(10)
            continue
        for file in unprocessed:
            presentation_path = os.path.join(config.UPLOADS_FOLDER, file + ".pptx")
            try:
                slides_text = extract_text_from_presentation(presentation_path)
                summaries = asyncio.run(process_presentation(slides_text, api_key))
                text_to_json_file(summaries, presentation_path, config.OUTPUTS_FOLDER)
                logger.info(f"Summarization completed for {file}.")
            except Exception as e:
                logger.error(f"Error processing file {file}: {e}")
        time.sleep(2)

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a PowerPoint presentation and summarize it")
    parser.add_argument("presentation_path", type=str, nargs="?", help="Relative path to the PowerPoint presentation file.")
    args = parser.parse_args()

    presentation_path = args.presentation_path
    if not presentation_path:
        running()
    
    logger.info(f"Relative presentation path: {presentation_path}")
    
    if not os.path.isfile(presentation_path):
        logger.error(f"Error: The presentation file '{presentation_path}' does not exist.")
        exit(1)

    api_key = get_key()

    try:
        slides_text = extract_text_from_presentation(presentation_path)
        summaries = asyncio.run(process_presentation(slides_text, api_key))
        text_to_json_file(summaries, presentation_path, config.OUTPUTS_FOLDER)
        logger.info("Summarization completed and saved to JSON file.")
    except Exception as e:
        logger.error(f"Error processing file {presentation_path}: {e}")

if __name__ == "__main__":
    main()
