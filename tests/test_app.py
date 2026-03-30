import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "ACEest Fitness" in data["message"]

def test_get_programs(client):
    response = client.get("/programs")
    assert response.status_code == 200
    data = response.get_json()
    assert "FL" in data
    assert data["FL"]["calorie_factor"] == 22
    assert "MG" in data
    assert data["MG"]["calorie_factor"] == 35
    assert "BG" in data
    assert data["BG"]["calorie_factor"] == 26
