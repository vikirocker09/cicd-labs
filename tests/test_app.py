import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_get_items(client):
    response = client.get('/items')
    assert response.status_code == 200

def test_add_item(client):
    response = client.post('/items', json={"name": "test item"})
    assert response.status_code in [200, 201]
