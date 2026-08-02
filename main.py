import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Customer Churn Prediction API")

# --- Dynamic & Absolute Model Path Resolution ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_NAMES = ["pipeline.pkl", "model.pkl", "model.joblib", "churn_pipeline.pkl"]
MODEL_PATH = None

for name in MODEL_NAMES:
    possible_path = os.path.join(BASE_DIR, name)
    if os.path.exists(possible_path):
        MODEL_PATH = possible_path
        break

pipeline = None
if MODEL_PATH:
    try:
        pipeline = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded successfully from: {MODEL_PATH}")
    except Exception as e:
        print(f"❌ Failed to load model from {MODEL_PATH}: {e}")
else:
    print("⚠️ No model file found in backend directory!")


# --- Input Schema matching Streamlit Frontend ---
class ChurnInput(BaseModel):
    MonthlyCharges: float
    TotalCharges: float
    Contract: str
    OnlineSecurity: str
    TechSupport: str
    PaperlessBilling: str
    Gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str


@app.get("/")
def home():
    return {"message": "Welcome to Customer Churn Prediction API! Go to /docs for Swagger UI."}


@app.post("/predict")
def predict(data: ChurnInput):
    if pipeline is None:
        raise HTTPException(
            status_code=500,
            detail="Pipeline not initialized. Ensure your .pkl/.joblib model file is tracked and pushed to GitHub."
        )

    try:
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict])

        prediction = pipeline.predict(input_df)[0]

        probability = None
        if hasattr(pipeline, "predict_proba"):
            probability = float(pipeline.predict_proba(input_df)[0][1])

        return {
            "prediction": int(prediction),
            "churn_risk": "High" if prediction == 1 else "Low",
            "churn_probability": probability
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction Error: {str(e)}")