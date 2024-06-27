import pytest
from web_api.scripts.app import app, generate_uid, get_current_time

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_generate_uid():
    uid1 = generate_uid()
    uid2 = generate_uid()
    assert isinstance(uid1, str)
    assert isinstance(uid2, str)
    assert uid1 != uid2

def test_get_current_time():
    time1 = get_current_time()
    time2 = get_current_time()
    assert isinstance(time1, str)
    assert isinstance(time2, str)
    assert time1 <= time2  # Time should be non-decreasing

def test_api_is_running(client):
    response = client.get('/')
    assert response.status_code == 404  # Because no endpoint is defined for '/'
