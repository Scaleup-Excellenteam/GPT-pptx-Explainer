import pytest
import os

import sys
import os

# הוספת נתיב הפרויקט ל-PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

@pytest.fixture(scope='session')
def demo_files_folder():
    folder = os.path.join(os.path.dirname(__file__), 'demo_files')
    os.makedirs(folder, exist_ok=True)
    return folder

@pytest.fixture(scope='session')
def outputs_folder():
    folder = os.path.join(os.path.dirname(__file__), 'outputs')
    os.makedirs(folder, exist_ok=True)
    return folder


@pytest.fixture(scope='session')
def uploads_folder():
    folder = os.path.join(os.path.dirname(__file__), '..', 'explainer', 'uploads')
    os.makedirs(folder, exist_ok=True)
    return folder

@pytest.fixture(scope='session')
def logs_folder():
    folder = os.path.join(os.path.dirname(__file__), '..', 'explainer', 'logs')
    os.makedirs(folder, exist_ok=True)
    return folder

@pytest.fixture(scope='session')
def web_api_outputs_folder():
    folder = os.path.join(os.path.dirname(__file__), '..', 'web_api', 'outputs')
    os.makedirs(folder, exist_ok=True)
    return folder

@pytest.fixture(scope='session')
def web_api_uploads_folder():
    folder = os.path.join(os.path.dirname(__file__), '..', 'web_api', 'uploads')
    os.makedirs(folder, exist_ok=True)
    return folder

@pytest.fixture(scope='session')
def web_api_logs_folder():
    folder = os.path.join(os.path.dirname(__file__), '..', 'web_api', 'logs')
    os.makedirs(folder, exist_ok=True)
    return folder
