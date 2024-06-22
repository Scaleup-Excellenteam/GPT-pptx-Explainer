import os
import pytest
import json
from pptx import Presentation
from pptx_extractor import extract_text_from_presentation, text_to_json_file
from async_tasks import process_presentation
from ai_api import load_api_key

@pytest.mark.asyncio
async def test_presentation_summary():
    """
    Test the summarization of a presentation with valid content.

    This test checks if the process can successfully extract text from a presentation,
    summarize it using OpenAI's API, and save the results to a JSON file.

    Raises:
        AssertionError: If any assertion fails.
    """
    presentation_path = r'pptx_files\DEMO.pptx'
    api_key = os.getenv("OPENAI_API_KEY")

    # Ensure the API key is set in the environment
    assert api_key is not None, "API key is not set in environment variables"

    slides_text = extract_text_from_presentation(presentation_path)
    summaries = await process_presentation(slides_text, api_key)
    text_to_json_file(summaries, presentation_path)

    # Check if the output file exists
    output_file = os.path.join('outputs', 'DEMO.json')
    assert os.path.isfile(output_file), "Output JSON file was not created"

    # Clean up: Remove the output file after the test
    if os.path.isfile(output_file):
        os.remove(output_file)

@pytest.mark.asyncio
async def test_empty_presentation():
    """
    Test the summarization of an empty presentation.

    This test checks if the process can handle an empty presentation file
    and produce an empty JSON file without errors.

    Raises:
        AssertionError: If any assertion fails.
    """
    presentation_path = 'EMPTY.pptx'
    api_key = os.getenv("OPENAI_API_KEY")

    # Create an empty pptx file for testing
    if not os.path.isfile(presentation_path):
        prs = Presentation()
        prs.save(presentation_path)

    assert api_key is not None, "API key is not set in environment variables"

    slides_text = extract_text_from_presentation(presentation_path)
    summaries = await process_presentation(slides_text, api_key)
    text_to_json_file(summaries, presentation_path)

    output_file = os.path.join('outputs', 'EMPTY.json')
    assert os.path.isfile(output_file), "Output JSON file was not created"

    with open(output_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 0, "Output JSON should be empty for an empty presentation"

    # Clean up: Remove the output file and the empty pptx file after the test
    if os.path.isfile(output_file):
        os.remove(output_file)
    if os.path.isfile(presentation_path):
        os.remove(presentation_path)

@pytest.mark.asyncio
async def test_missing_presentation():
    """
    Test the behavior when the presentation file is missing.

    This test ensures that a FileNotFoundError is raised when trying to process a non-existent presentation file.

    Raises:
        AssertionError: If any assertion fails.
    """
    presentation_path = 'MISSING.pptx'
    api_key = os.getenv("OPENAI_API_KEY")

    assert api_key is not None, "API key is not set in environment variables"

    with pytest.raises(FileNotFoundError):
        slides_text = extract_text_from_presentation(presentation_path)
        await process_presentation(slides_text, api_key)

@pytest.mark.asyncio
async def test_malformed_presentation():
    """
    Test the behavior when the presentation file is malformed.

    This test ensures that an exception is raised when trying to process a malformed presentation file.

    Raises:
        AssertionError: If any assertion fails.
    """
    presentation_path = 'MALFORMED.pptx'
    api_key = os.getenv("OPENAI_API_KEY")

    # Create a malformed pptx file for testing
    if not os.path.isfile(presentation_path):
        with open(presentation_path, 'w') as file:
            file.write("This is not a valid pptx file content")

    assert api_key is not None, "API key is not set in environment variables"

    with pytest.raises(Exception):
        slides_text = extract_text_from_presentation(presentation_path)
        await process_presentation(slides_text, api_key)

    # Clean up: Remove the malformed pptx file after the test
    if os.path.isfile(presentation_path):
        os.remove(presentation_path)
