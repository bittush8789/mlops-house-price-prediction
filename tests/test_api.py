from fastapi.testclient import TestClient
from main import app
import pytest

def test_home_endpoint():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

def test_prediction_endpoint():
    client = TestClient(app)
    payload = {
        "area_sqft": 1500,
        "bedrooms": 2,
        "bathrooms": 2,
        "floors": 1,
        "parking": 1,
        "year_built": 2015,
        "location": "Noida",
        "sub_location": "Sector 50",
        "furnishing": "Semi-Furnished",
        "property_type": "Apartment"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    
    json_data = response.json()
    assert "predicted_price" in json_data
    assert "market_tier" in json_data
    assert "confidence_level" in json_data
    assert "price_per_sqft" in json_data
    assert "ai_factors" in json_data

def test_prediction_invalid_data():
    client = TestClient(app)
    payload = {"area_sqft": "invalid"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422 # Validation Error
