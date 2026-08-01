from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_single_prediction():
    payload = {
        "tenure_months": 12,
        "monthly_charges": 85.5,
        "total_charges": 1026.0,
        "num_support_tickets": 2,
        "contract_type": "month-to-month",
        "payment_method": "electronic_check",
        "tech_support": "no"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "churn_prediction" in response.json()
    assert "churn_risk_level" in response.json()