from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI(title="Customer Churn Prediction API")

# Load the saved model
with open('xgboost_churn_model.pkl', 'rb') as f:
    model = pickle.load(f)

class CustomerData(BaseModel):
    tenure_months: int
    monthly_charges: float
    num_support_tickets: int
    is_contract_month_to_month: int

@app.get("/")
def home():
    return {"message": "Welcome to Customer Churn Prediction API"}

@app.post("/predict")
def predict_churn(customer: CustomerData):
    input_data = np.array([[
        customer.tenure_months,
        customer.monthly_charges,
        customer.num_support_tickets,
        customer.is_contract_month_to_month
    ]])
    
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    
    result = "Customer will leave (Churn)" if prediction == 1 else "Customer will stay"
    
    return {
        "prediction": result,
        "churn_probability": round(float(probability), 2)
    }
from fastapi import FastAPI, HTTPException, status

import os
import joblib

# Resolve the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "pipeline.pkl") # Ensure filename matches yours

try:
    pipeline = joblib.load(MODEL_PATH)
except Exception as e:
    pipeline = None
    print(f"Error loading pipeline model: {e}")

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint for Docker/Kubernetes probes."""
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Model pipeline artifact is missing or not loaded."
        )
    return {"status": "healthy", "model_version": "2.0.0"}

def calculate_risk_level(prob: float) -> str:
    if prob >= 0.70:
        return "High Risk"
    elif prob >= 0.35:
        return "Medium Risk"
    return "Low Risk"

@app.post("/predict", response_model=PredictionResponse)
def predict_single(customer: CustomerInput):
    """Real-time inference endpoint for a single customer."""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized.")
    
    # Convert input schema directly to DataFrame
    input_df = pd.DataFrame([customer.model_dump()])
    
    # Run through full Scikit-Learn pipeline
    proba = float(pipeline.predict_proba(input_df)[0][1])
    pred = int(proba > 0.5)
    
    return PredictionResponse(
        churn_prediction=pred,
        churn_risk_level=calculate_risk_level(proba),
        churn_probability=round(proba, 4)
    )

@app.post("/predict/batch", response_model=List[PredictionResponse])
def predict_batch(batch: BatchCustomerInput):
    """Batch inference endpoint for bulk customer data processing."""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized.")
    
    input_df = pd.DataFrame([c.model_dump() for c in batch.customers])
    probas = pipeline.predict_proba(input_df)[:, 1]
    
    results = []
    for proba in probas:
        p_val = float(proba)
        results.append(PredictionResponse(
            churn_prediction=int(p_val > 0.5),
            churn_risk_level=calculate_risk_level(p_val),
            churn_probability=round(p_val, 4)
        ))
    
    return results
@app.get("/")
def home():
    return {"message": "Welcome to Customer Churn Prediction API! Go to /docs for Swagger UI."}