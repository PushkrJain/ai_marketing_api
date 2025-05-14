import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app


client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Marketing API is running!"}

def test_token_and_auth():
    # Get token
    response = client.post("/token", data={"username": "alice", "password": "wonderland"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Access protected endpoint (if /feedbacks is protected)
    response = client.get("/feedbacks", headers=headers)
    assert response.status_code == 200
    assert "feedbacks" in response.json()

def test_create_campaign_and_feedback():
    # Get JWT token first
    login = client.post(
        "/token",
        data={"username": "alice", "password": "wonderland"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    # Create a campaign with feedback
    campaign = {
        "customer_profile": {"name": "TestUser", "interests": ["test"]},
        "campaign_type": "email",
        "product": "TestProduct",
        "offer": "TestOffer",
        "feedback": {"rating": 5, "comment": "Great!"},
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/create-campaign", json=campaign,
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "generated_content" in response.json()
