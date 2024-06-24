import argparse
import time
import asyncio
import os
from pptx_extractor import extract_text_from_presentation, text_to_json_file
from async_tasks import process_presentation
from ai_api import load_api_key


UPLOADS_FOLDER = r"uploads"
OUTPUTS_FOLDER = r"outputs"


def get_key():
    api_key = load_api_key()
    if not api_key:
        print("Error: The OpenAI API key is not set in the environment variables.")
        exit(1)
    print("Loaded OpenAI API key from environment.")
    return api_key


def get_unprocessed_files():
    print(f"Checking for unprocessed files in {UPLOADS_FOLDER}.")
    process_presentation = {file.split(".")[0] for file in os.listdir(UPLOADS_FOLDER)}
    all_files = {file.split(".")[0] for file in os.listdir(OUTPUTS_FOLDER)}
    return process_presentation - all_files
    

def runnig():
    api_key = load_api_key()
    while True:
        unprocessed = get_unprocessed_files()
        if not unprocessed:
            time.sleep(10)
        for file in unprocessed:
            presentation_path = os.path.join(UPLOADS_FOLDER, file + ".pptx")
            slides_text = extract_text_from_presentation(presentation_path)
            summaries = asyncio.run(process_presentation(slides_text, api_key))
            text_to_json_file(summaries, presentation_path)
            print(f"Summarization completed for {file}.")
        time.sleep(2)
    
        
        



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Extract text from a PowerPoint presentation and summarize it")
    parser.add_argument("presentation_path", type=str, nargs="?", help="Relative path to the PowerPoint presentation file.")
    args = parser.parse_args()

    presentation_path = args.presentation_path
    if not presentation_path:
        runnig()
        exit(0)
        
    print(f"Relative presentation path: {presentation_path}")
    
    if not os.path.isfile(presentation_path):
        print(f"Error: The presentation file '{presentation_path}' does not exist.")
        exit(1)

    api_key = get_key()

    slides_text = extract_text_from_presentation(presentation_path)
    summaries = asyncio.run(process_presentation(slides_text, api_key))
    text_to_json_file(summaries, presentation_path)
    print("Summarization completed and saved to JSON file.")
