import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app  # Adjust import if your app is in a different module

client = TestClient(app)

USERNAME = "alice"
PASSWORD = "wonderland"

def get_token():
    response = client.post(
        "/token",
        data={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200, f"Token error: {response.text}"
    return response.json()["access_token"]

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_token_and_auth():
    token = get_token()
    assert token is not None and isinstance(token, str)

def test_protected_create_campaign():
    token = get_token()
    payload = {
        "customer_profile": {
            "name": USERNAME,
            "interests": ["Tech", "Shoes"],
            "age": 30,
            "location": "urban"
        },
        "campaign_type": "email",
        "product": "Shoes",
        "offer": "50% off",
        "feedback": {"click_rate": 0.1}
    }
    response = client.post(
        "/create-campaign",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "generated_content" in response.json()

def test_feedback_persistence():
    token = get_token()
    feedback = {"click_rate": 0.5, "comment": "Great!"}
    payload = {
        "customer_profile": {
            "name": USERNAME,
            "interests": ["Tech"],
            "age": 28,
            "location": "city"
        },
        "campaign_type": "sms",
        "product": "Watch",
        "offer": "10% off",
        "feedback": feedback
    }
    # Submit feedback
    response = client.post(
        "/create-campaign",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_generate_content():
    payload = {
        "customer_name": USERNAME,
        "segments": ["Tech", "Shoes"],
        "campaign_type": "email",
        "product": "Shoes",
        "offer": "50% off"
    }
    response = client.post("/generate-content", json=payload)
    assert response.status_code == 200
    assert "generated_content" in response.json()

def test_segment():
    payload = {"age": 30, "interests": ["Tech"], "location": "urban"}
    response = client.post("/segment", json=payload)
    assert response.status_code == 200
    assert "segments" in response.json()

def test_optimize():
    payload = {
        "original_prompt": "Test prompt",
        "feedback": {"comment": "Make it better"},
        "strategy": "engagement_boost"
    }
    response = client.post("/optimize", json=payload)
    assert response.status_code == 200
    assert "optimized_prompt" in response.json()

def test_auth_required():
    # Should fail without token
    payload = {
        "customer_profile": {"name": USERNAME},
        "campaign_type": "email",
        "product": "Shoes",
        "offer": "50% off"
    }
    response = client.post("/create-campaign", json=payload)
    assert response.status_code in (401, 403)

def test_invalid_token():
    payload = {
        "customer_profile": {"name": USERNAME},
        "campaign_type": "email",
        "product": "Shoes",
        "offer": "50% off"
    }
    response = client.post(
        "/create-campaign",
        json=payload,
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code in (401, 403)
