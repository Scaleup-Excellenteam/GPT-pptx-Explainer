import os
import pytest
import json
from pptx import Presentation
from explainer.scripts.pptx_extractor import extract_text_from_presentation, text_to_json_file
from explainer.scripts.async_tasks import process_presentation
from explainer.scripts.ai_api import load_api_key

@pytest.mark.asyncio
async def test_empty_presentation(demo_files_folder, outputs_folder):
    presentation_path = os.path.join(demo_files_folder, 'EMPTY.pptx')
    api_key = os.getenv("OPENAI_API_KEY")

    if not os.path.isfile(presentation_path):
        prs = Presentation()
        prs.save(presentation_path)

    assert api_key is not None, "API key is not set in environment variables"

    slides_text = extract_text_from_presentation(presentation_path)
    summaries = await process_presentation(slides_text, api_key)
    text_to_json_file(summaries, presentation_path, output_dir=outputs_folder)
    
    output_file = os.path.join(outputs_folder, 'EMPTY.json')
    assert os.path.isfile(output_file), "Output JSON file was not created"

    with open(output_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 0, "Output JSON should be empty for an empty presentation"

    if os.path.isfile(output_file):
        os.remove(output_file)
    if os.path.isfile(presentation_path):
        os.remove(presentation_path)

@pytest.mark.asyncio
async def test_missing_presentation(demo_files_folder):
    presentation_path = os.path.join(demo_files_folder, 'MISSING.pptx')
    api_key = os.getenv("OPENAI_API_KEY")

    assert api_key is not None, "API key is not set in environment variables"

    with pytest.raises(FileNotFoundError):
        slides_text = extract_text_from_presentation(presentation_path)
        await process_presentation(slides_text, api_key)

@pytest.mark.asyncio
async def test_malformed_presentation(demo_files_folder):
    presentation_path = os.path.join(demo_files_folder, 'MALFORMED.pptx')
    api_key = os.getenv("OPENAI_API_KEY")

    if not os.path.isfile(presentation_path):
        with open(presentation_path, 'w') as file:
            file.write("This is not a valid pptx file content")

    assert api_key is not None, "API key is not set in environment variables"

    with pytest.raises(Exception):
        slides_text = extract_text_from_presentation(presentation_path)
        await process_presentation(slides_text, api_key)

    if os.path.isfile(presentation_path):
        os.remove(presentation_path)
