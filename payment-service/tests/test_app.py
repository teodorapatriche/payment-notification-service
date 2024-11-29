import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_process_payment(client):
    # Valid request
    response = client.post('/pay', json={"amount": 5000, "currency": "gbp"})
    assert response.status_code == 200
    assert "clientSecret" in response.get_json()

    # Invalid amount
    response = client.post('/pay', json={"amount": -5000, "currency": "gbp"})
    assert response.status_code == 400
    assert "error" in response.get_json()

    # Missing fields
    response = client.post('/pay', json={"currency": "gbp"})
    assert response.status_code == 400
