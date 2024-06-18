# README - GPT PPTX Summerizer

## Overview

GPT-Explainer is a Python script designed to help computer science students understand their lecture presentations better. The script takes a PowerPoint presentation (`.pptx` file) as input, sends the text from each slide to the GPT-3.5 AI model, and saves the summarized results in a JSON file. This tool can be particularly useful for clarifying complex concepts and providing detailed explanations.

## Features

- Extracts text from PowerPoint presentations.
- Summarizes the content using OpenAI's GPT-3.5 AI model.
- Handles slides with multiple text boxes.
- Creates asynchronous API calls for faster processing.
- Saves the summarized text in a JSON file.
- Handles errors gracefully and continues processing other slides.
- CLI interface for ease of use.

## Requirements

- Python 3.7+
- `openai` Python package
- `python-pptx` Python package
- `pytest` Python package for testing

## Usage

You can run the script using the command line:
bash
python main.py <relative_path>

Alternatively, you can run it directly and provide the paths when prompted:

```bash
python main.py
```
and then input from stdin <relative_path>


## File Structure

- `main.py`: The main script that handles input, calls the processing functions, and outputs the results.
- `pptx_extractor.py`: Contains functions to extract text from the presentation and create asynchronous tasks.
- `ai_summery.py`: Contains functions to interact with the OpenAI API and generate summaries.
- `test_pptx_extractor_ai_summery.py`: Contains tests to verify the functionality of the script.

## Examples

To summarize a presentation located at `DEMO.pptx`, run:

```bash
python main.py DEMO.pptx
```

The output JSON file will be saved in the `outputs` directory with the same name as the input file (e.g., `DEMO.json`).

## Testing

To run the tests, use the following command:

```bash
pytest test_pptx_extractor_ai_summery.py
```

The tests include:
- `test_presentation_summary`: Tests the summarization of a valid presentation.
- `test_empty_presentation`: Tests handling of an empty presentation.
- `test_missing_presentation`: Tests handling of a non-existent presentation file.
- `test_malformed_presentation`: Tests handling of a malformed presentation file.

## Error Handling

The script includes error handling for:
- Missing or incorrect file paths.
- Issues with loading the presentation file.
- Timeouts during the API calls.
- Slides without text.

