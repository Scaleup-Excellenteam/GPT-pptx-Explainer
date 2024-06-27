import pytest
from client.scripts.client import Status
from unittest.mock import patch
import os


@pytest.fixture
def requests_mock():
    with patch('client.scripts.client.requests') as mock:
        yield mock

def test_upload_file(requests_mock):
    requests_mock.post.return_value.status_code = 200
    requests_mock.post.return_value.json.return_value = {'uid': '12345'}
    
    file_path = 'tests/demo_files/DEMO.pptx'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write('dummy content')

    uid = Status.upload_file(file_path)
    assert uid == '12345'


def test_get_status_completed(requests_mock):
    requests_mock.get.return_value.status_code = 200
    requests_mock.get.return_value.json.return_value = {
        'status': 'completed',
        'filename': 'DEMO',
        'timestamp': '2024-06-27[12-00-00]',
        'summaries': {'summary': 'summary content'}
    }
    
    uid = '12345'
    status = Status.get_status(uid)
    assert status.is_completed()
    assert status.summaries == {'summary': 'summary content'}

def test_get_status_in_progress(requests_mock):
    requests_mock.get.return_value.status_code = 200
    requests_mock.get.return_value.json.return_value = {
        'status': 'in progress',
        'filename': 'DEMO',
        'timestamp': '2024-06-27[12-00-00]',
        'summaries': None
    }
    
    uid = '12345'
    status = Status.get_status(uid)
    assert not status.is_completed()
    assert status.summaries is None




