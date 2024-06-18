import pptx_extractor
import argparse
import asyncio
import os


def load_and_print_api_key():
    api_key = os.getenv("OPENAI_PRIVATE_KEY")
    print(f"Loaded OpenAI API key from environment: {api_key}")
    return api_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="extract text from a PowerPoint presentation and summarize it")
    parser.add_argument("presentation_path", type=str, nargs="?", help="relative path to the powerPoint presentation file.",)
    args = parser.parse_args()

    presentation_path = args.presentation_path
    if not presentation_path:
        presentation_path = input("Please Enter relative path to the PowerPoint presentation file: ")
    print(f"relative presentation path: {presentation_path}")
    
    if not os.path.isfile(presentation_path):
        print(f"Error: The presentation file '{presentation_path}' does not exist.")
        exit(1)

    api_key = load_and_print_api_key()
    if not api_key:
        print("Error: The OpenAI API key is not set in the environment variables.")
        exit(1)
    text = asyncio.run(pptx_extractor.extract_text_from_presentation(presentation_path, api_key))
    pptx_extractor.text_to_json_file(text, presentation_path)
