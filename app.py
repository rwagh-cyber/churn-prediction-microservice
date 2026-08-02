import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Prediction", page_icon="🚀", layout="wide")

st.title("📊 Customer Churn Prediction Dashboard")
st.write("Fill in customer details below to estimate churn risk.")

# --- UI Input Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    tenure_months = st.number_input("Tenure (Months)", min_value=0, max_value=120, value=12)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=65.50)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=786.00)
    contract = st.selectbox("Contract Type", ["month-to-month", "One year", "Two year"])

with col2:
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["yes", "no", "No internet service"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment_method = st.selectbox("Payment Method", [
        "Electronic check", 
        "Mailed check", 
        "Bank transfer (automatic)", 
        "Credit card (automatic)"
    ])

with col3:
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior_citizen = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])

# --- Predict Action ---
if st.button("🚀 Predict Churn Risk"):
    BACKEND_URL = "https://churn-prediction-microservice.onrender.com/predict"

    payload = {
        "tenure_months": tenure_months,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "Contract": contract,
        "OnlineSecurity": online_security,
        "TechSupport": tech_support,
        "PaperlessBilling": paperless_billing,
        "payment_method": payment_method,
        "Gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents
    }

    with st.spinner("Connecting to FastAPI backend..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=30)

            if response.status_code == 200:
                res = response.json()
                risk = res.get("churn_risk", "Unknown")
                prob = res.get("churn_probability")

                st.subheader("Prediction Result:")
                if risk == "High":
                    st.error(f"⚠️ Churn Risk: **{risk}**")
                else:
                    st.success(f"✅ Churn Risk: **{risk}**")

                if prob is not None:
                    st.metric(label="Churn Probability", value=f"{prob * 100:.1f}%")

            else:
                st.error(f"FastAPI Server returned status code: {response.status_code}")
                st.code(response.text)

        except requests.exceptions.RequestException as err:
            st.error(f"Failed to reach FastAPI backend: {err}")