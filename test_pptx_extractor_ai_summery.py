import os
import pytest
import json
import asyncio
from pptx import Presentation
import pptx_extractor

@pytest.mark.asyncio
async def test_presentation_summary():
    presentation_path = 'DEMO.pptx'
    api_key = os.getenv("OPENAI_PRIVATE_KEY")

    # Ensure the API key is set in the environment
    assert api_key is not None, "API key is not set in environment variables"

    # Run the main script functionality
    text = await pptx_extractor.extract_text_from_presentation(presentation_path, api_key)
    pptx_extractor.text_to_json_file(text, presentation_path)

    # Check if the output file exists
    output_file = os.path.join('outputs', 'DEMO.json')
    assert os.path.isfile(output_file), "Output JSON file was not created"

    # Clean up: Remove the output file after the test
    if os.path.isfile(output_file):
        os.remove(output_file)

@pytest.mark.asyncio
async def test_empty_presentation():
    presentation_path = 'EMPTY.pptx'
    api_key = os.getenv("OPENAI_PRIVATE_KEY")

    # Create an empty pptx file for testing
    if not os.path.isfile(presentation_path):
        prs = Presentation()
        prs.save(presentation_path)

    assert api_key is not None, "API key is not set in environment variables"

    text = await pptx_extractor.extract_text_from_presentation(presentation_path, api_key)
    pptx_extractor.text_to_json_file(text, presentation_path)

    output_file = os.path.join('outputs', 'EMPTY.json')
    assert os.path.isfile(output_file), "Output JSON file was not created"

    with open(output_file, 'r') as file:
        data = json.load(file)
        assert len(data) == 0, "Output JSON should be empty for an empty presentation"

    # Clean up: Remove the output file and the empty pptx file after the test
    if os.path.isfile(output_file):
        os.remove(output_file)
    if os.path.isfile(presentation_path):
        os.remove(presentation_path)

@pytest.mark.asyncio
async def test_missing_presentation():
    presentation_path = 'MISSING.pptx'
    api_key = os.getenv("OPENAI_PRIVATE_KEY")

    assert api_key is not None, "API key is not set in environment variables"

    with pytest.raises(FileNotFoundError):
        await pptx_extractor.extract_text_from_presentation(presentation_path, api_key)

@pytest.mark.asyncio
async def test_malformed_presentation():
    presentation_path = 'MALFORMED.pptx'
    api_key = os.getenv("OPENAI_PRIVATE_KEY")

    # Create a malformed pptx file for testing
    if not os.path.isfile(presentation_path):
        with open(presentation_path, 'w') as file:
            file.write("This is not a valid pptx file content")

    assert api_key is not None, "API key is not set in environment variables"

    with pytest.raises(Exception):
        await pptx_extractor.extract_text_from_presentation(presentation_path, api_key)

    # Clean up: Remove the malformed pptx file after the test
    if os.path.isfile(presentation_path):
        os.remove(presentation_path)
