import pytest
from app import app

@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(test_client):
    res = test_client.get("/")
    assert res.status_code == 200
    
    html = res.get_data(as_text=True)
    assert "ACEest Fitness" in html
    assert "ACHIEVE. TRAIN." in html
    assert "SUCCEED." in html

def test_programs_endpoint(test_client):
    res = test_client.get("/programs")
    assert res.status_code == 200
    
    data = res.get_json()
    
    assert "FL" in data
    assert data["FL"]["calorie_factor"] == 22
    
    assert "MG" in data
    assert data["MG"]["calorie_factor"] == 35
    
    assert "BG" in data
    assert data["BG"]["calorie_factor"] == 26
