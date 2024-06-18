import pptx_extractor
import ai_summery
import argparse
import asyncio
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract text from a PowerPoint presentation and summarize it using OpenAI's GPT.")
    parser.add_argument('presentation_path', type=str, nargs='?', help='Absolute path to the PowerPoint presentation file.')
    parser.add_argument('api_key_path', type=str, nargs='?', help='Absolute path to the file containing the OpenAI API key.')
    args = parser.parse_args()

    presentation_path = args.presentation_path
    api_key_path = args.api_key_path

    if not presentation_path:
        presentation_path = input("Enter the absolute path to the PowerPoint presentation file: ")
    if not api_key_path:
        api_key_path = input("Enter the absolute path to the file containing the OpenAI API key: ")

    if not os.path.isfile(presentation_path):
        print(f"Error: The presentation file '{presentation_path}' does not exist.")
        exit(1)
    if not os.path.isfile(api_key_path):
        print(f"Error: The API key file '{api_key_path}' does not exist.")
        exit(1)

    api_key = ai_summery.load_api_key(api_key_path)
    text = asyncio.run(pptx_extractor.extract_text_from_presentation(presentation_path, api_key))
    pptx_extractor.text_to_json_file(text, presentation_path)
