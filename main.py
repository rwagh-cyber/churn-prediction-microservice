import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Customer Churn Prediction API")

# Path set to actual model file name from your repository
MODEL_PATH = os.path.join(os.path.dirname(__file__), "churn_pipeline.joblib")

# Try loading pipeline first, fallback to xgboost file if needed
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully from churn_pipeline.joblib!")
except Exception as e:
    try:
        ALT_PATH = os.path.join(os.path.dirname(__file__), "xgboost_churn_model.pkl")
        model = joblib.load(ALT_PATH)
        print("Model loaded from xgboost_churn_model.pkl!")
    except Exception as err:
        print(f"Error loading models: {err}")
        model = None

class CustomerInput(BaseModel):
    tenure_months: int
    monthly_charges: float
    total_charges: float
    num_support_tickets: int
    contract_type: str
    payment_method: str
    tech_support: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/predict")
@app.post("/predict/")
def predict(data: CustomerInput):
    if model is None:
        raise HTTPException(
            status_code=500, 
            detail="ML Model file not found on server. Please check repository files."
        )

    try:
        input_dict = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        
        # Value formatting for ML Model
        contract_map = {
            "month-to-month": "Month-to-month",
            "one_year": "One year",
            "two_year": "Two year"
        }
        payment_map = {
            "electronic_check": "Electronic check",
            "mailed_check": "Mailed check",
            "bank_transfer": "Bank transfer (automatic)",
            "credit_card": "Credit card (automatic)"
        }
        
        c_type = str(input_dict["contract_type"]).lower()
        p_method = str(input_dict["payment_method"]).lower()
        t_support = str(input_dict["tech_support"]).lower()

        input_dict["contract_type"] = contract_map.get(c_type, input_dict["contract_type"].title())
        input_dict["payment_method"] = payment_map.get(p_method, input_dict["payment_method"].title())
        input_dict["tech_support"] = "No" if t_support == "no" else ("Yes" if t_support == "yes" else input_dict["tech_support"].title())

        df = pd.DataFrame([input_dict])

        # Real ML Model Prediction
        prediction = int(model.predict(df)[0])
        
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(df)[0][1])
        else:
            probability = float(prediction)

        risk_level = "High" if prediction == 1 else "Low"

        return {
            "churn_prediction": prediction,
            "prediction": prediction,
            "churn_risk_level": risk_level,
            "churn_risk": risk_level,
            "churn_probability": probability
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))