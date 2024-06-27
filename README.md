

---

# README - GPT PPTX Summarizer

## Overview

GPT-Explainer is a Python-based project designed to assist computer science students in understanding their lecture presentations more effectively. The script takes a PowerPoint presentation (`.pptx` file), extracts the text from each slide, sends the text to the GPT-3.5 AI model, and saves the summarized results in a JSON file. This tool is particularly useful for clarifying complex concepts and providing detailed explanations.

## Setup

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/final-exercise-DSH93.git
    cd final-exercise-DSH93
    ```

2. Install the package:
    ```sh
    pip install .
    ```

### Configuration

The project uses configuration files for different modules. Ensure you have the following files in the `configs` directory:

- `client_config.py`
- `explainer_config.py`
- `web_api_config.py`

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

### Running All Modules

You can run all the modules simultaneously using the provided `run_all.exe`. Simply execute:
```sh
run_all.exe
```

## File Structure

The project is structured as follows:

```
final-exercise-DSH93/
    ├── client/
    │    ├── logs/
    │    ├── pptx_files/
    │    ├── scripts/
    │    │    ├── client.py
    │    │    └── __init__.py
    │    └── __init__.py
    ├── configs/
    │    ├── __init__.py
    │    ├── client_config.py
    │    ├── explainer_config.py
    │    ├── web_api_config.py
    ├── explainer/
    │    ├── logs/
    │    ├── outputs/
    │    ├── uploads/
    │    ├── scripts/
    │    │    ├── ai_api.py
    │    │    ├── async_tasks.py
    │    │    ├── main.py
    │    │    ├── pptx_extractor.py
    │    │    └── __init__.py
    │    └── __init__.py
    ├── run_all_module/
    │    ├── __init__.py
    │    ├── run_all.py
    ├── tests/
    │    ├── demo_files/
    │    │    └── DEMO.pptx  
    │    ├── outputs/
    │    ├── uploads/   
    │    ├── conftest.py
    │    ├── test_client.py
    │    ├── test_explainer.py
    │    └── test_web_api.py
    ├── web_api/
    │    ├── logs/
    │    ├── scripts/
    │    │    ├── app.py
    │    │    └── __init__.py
    │    └── __init__.py
    ├── .gitignore
    ├── pyproject.toml
    ├── README.md
    ├── requirements.txt
    └── setup.py
```

## Testing

To run the tests, navigate to the `tests` directory and use the following command:

```bash
pytest
```

### Tests Include:

- **Client Tests** (`test_client.py`)
  - `test_upload_file`: Tests the file upload functionality.
  - `test_get_status_completed`: Tests fetching the status when processing is completed.
  - `test_get_status_in_progress`: Tests fetching the status when processing is in progress.

- **Explainer Tests** (`test_explainer.py`)
  - `test_empty_presentation`: Tests handling of an empty presentation.
  - `test_missing_presentation`: Tests handling of a non-existent presentation file.
  - `test_malformed_presentation`: Tests handling of a malformed presentation file.

- **Web API Tests** (`test_web_api.py`)
  - `test_upload_file`: Tests the file upload endpoint.
  - `test_get_status_completed`: Tests the status endpoint for completed files.
  - `test_get_status_in_progress`: Tests the status endpoint for files in progress.

## Error Handling

The script includes error handling for:
- Missing or incorrect file paths.
- Issues with loading the presentation file.
- Timeouts during the API calls.
- Slides without text.

## Logging

Logs are written to files in the `logs` directory within the `client`, `explainer`, and `web_api` directories. Logs are rotated daily and kept for up to 5 days. Ensure that the `LOGS_FOLDER` is created and set up correctly in the configuration files for proper logging.

---

This README provides a comprehensive guide to setting up, running, and testing the GPT PPTX Summarizer project. Make sure to follow the instructions carefully to ensure the project runs smoothly.