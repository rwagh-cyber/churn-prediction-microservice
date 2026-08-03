from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Customer Churn Prediction API")

# Load your trained model (make sure the filename matches your actual model file)
try:
    model = joblib.load("model.pkl")  # किंवा तुझ्या मॉडेल फाईलचे नाव (उदा. churn_model.pkl)
except Exception as e:
    model = None

# Pydantic Schema strictly matching ML Model's expected 7 features
class CustomerInput(BaseModel):
    tenure_months: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    tech_support: str
    payment_method: str
    num_support_tickets: int

@app.get("/")
def read_root():
    return {"message": "Welcome to Customer Churn Prediction API! Go to /docs for Swagger UI."}

@app.post("/predict/")
def predict(data: CustomerInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded on server.")
    
    try:
        # Convert incoming JSON payload to DataFrame
        input_data = data.dict()
        df = pd.DataFrame([input_data])

        # Model Prediction
        prediction = int(model.predict(df)[0])
        
        probability = None
        if hasattr(model, "predict_proba"):
            prob_array = model.predict_proba(df)[0]
            probability = float(prob_array[1])

        churn_risk = "High" if prediction == 1 else "Low"

        return {
            "prediction": prediction,
            "churn_risk": churn_risk,
            "churn_probability": probability
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction Error: {str(e)}")