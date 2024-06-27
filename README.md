# README - GPT PPTX Summarizer

## Overview

GPT-Explainer is a Python-based project designed to assist computer science students in understanding their lecture presentations more effectively. The script takes a PowerPoint presentation (`.pptx` file), extracts the text from each slide, sends the text to the GPT-3.5 AI model, and saves the summarized results in a JSON file. This tool is particularly useful for clarifying complex concepts and providing detailed explanations.

## Usage Instructions

### 1. Web API

1. Open a terminal in the `final-exercise-DSH93` directory.
2. Run the following command to start the Web API:

    ```sh
    python ./web_api/scripts/app.py
    ```

### 2. Explainer

1. Open a new terminal in the `final-exercise-DSH93\explainer` directory.
2. Run the following command to start the Explainer script:

    ```sh
    python ./scripts/main.py
    ```

### 3. Client

1. Open a new terminal in the `final-exercise-DSH93\client` directory.
2. Run the following command to start the client:

    ```sh
    python ./scripts/client.py
    ```
3. Use the interactive interface to upload files or check their status:
   - To use a file, enter the full path.
   - If the file is in the `pptx_files` directory, enter the relative path:

    ```sh
    pptx_files\example_name.pptx
    ```

## File Structure

The project is structured as follows:

```
final-exercise-DSH93/
    ├── client/
    |    ├── logs/
    │    ├── pptx_files/
    │    ├── scripts/
    │    |    ├── client.py
    |    |    └── __init__.py
    |    |
    |    └── __init__.py
    |
    ├── explainer/
    │    ├── logs/
    │    ├── outputs/
    │    ├── uploads/
    │    ├── scripts/
    │    |    ├── ai_api.py
    │    |    ├── async_tasks.py
    │    |    ├── main.py
    │    |    ├──pptx_extractor.py
    |    |    └── __init__.py
    |    └── __init__.py
    |
    ├── tests/
    │    ├── demo_files/
    │    │    └── DEMO.pptx  
    │    ├── outputs/
    |    ├── conftest.py
    |    ├── test_client.py
    |    ├── test_explainer.py
    │    └── test_web_api.py
    |
    ├── web_api/
    |    ├── logs/
    │    ├── scripts/
    │    |     ├── app.py
    |    |     └── __init__.py
    |    └── __init__.py
    |
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    └── setup.py
```

## Testing

To run the tests, navigate to the `tests` directory and use the following command:

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

## Logging

Logs are written to files in the `logs` directory within the `explainer` and `web_api` directories. Logs are rotated daily and kept for up to 5 days. Ensure that the `LOGS_FOLDER` is created and set up correctly in both the `main.py` and `app.py` scripts for proper logging.

---

This README provides a comprehensive guide to setting up, running, and testing the GPT PPTX Summarizer project. Make sure to follow the instructions carefully to ensure the project runs smoothly.