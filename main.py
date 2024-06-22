import argparse
import asyncio
import os
from pptx_extractor import extract_text_from_presentation, text_to_json_file
from async_tasks import process_presentation
from ai_api import load_api_key

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract text from a PowerPoint presentation and summarize it")
    parser.add_argument("presentation_path", type=str, nargs="?", help="Relative path to the PowerPoint presentation file.")
    args = parser.parse_args()

    presentation_path = args.presentation_path
    if not presentation_path:
        presentation_path = input("Please Enter relative path to the PowerPoint presentation file: ")
    print(f"Relative presentation path: {presentation_path}")
    
    if not os.path.isfile(presentation_path):
        print(f"Error: The presentation file '{presentation_path}' does not exist.")
        exit(1)

    api_key = load_api_key()
    if not api_key:
        print("Error: The OpenAI API key is not set in the environment variables.")
        exit(1)
    print("Loaded OpenAI API key from environment.")

    slides_text = extract_text_from_presentation(presentation_path)
    summaries = asyncio.run(process_presentation(slides_text, api_key))
    text_to_json_file(summaries, presentation_path)
    print("Summarization completed and saved to JSON file.")
