import pytest
from app import app  # Import the Flask app from app.py

@pytest.fixture
def client():
    # Create a test client for the Flask app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello(client):
    # Test the root endpoint '/'
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Hello, World!"  # Flask responses are byte strings