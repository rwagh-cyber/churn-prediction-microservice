import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Prediction", page_icon="🚀", layout="wide")

st.title("📊 Customer Churn Prediction Dashboard")
st.write("Fill in customer details below to estimate churn risk.")

# Input Layout
col1, col2, col3 = st.columns(3)

with col1:
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=65.50)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=786.00)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])

with col2:
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    gender = st.selectbox("Gender", ["Male", "Female"])

with col3:
    senior_citizen = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])

# Predict Button
if st.button("🚀 Predict Churn Risk"):
    # exact URL
    BACKEND_URL = "https://churn-prediction-microservice-3.onrender.com/predict/"

    payload = {
        "MonthlyCharges": float(monthly_charges),
        "TotalCharges": float(total_charges),
        "Contract": contract,
        "OnlineSecurity": online_security,
        "TechSupport": tech_support,
        "PaperlessBilling": paperless_billing,
        "Gender": gender,
        "SeniorCitizen": int(senior_citizen),
        "Partner": partner,
        "Dependents": dependents
    }

    with st.spinner("Connecting to FastAPI backend..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=30)

            if response.status_code == 200:
                res = response.json()
                
                prediction = res.get("prediction")
                churn_risk = res.get("churn_risk", "Unknown")
                churn_prob = res.get("churn_probability")

                st.subheader("Prediction Result:")
                if churn_risk == "High" or prediction == 1:
                    st.error(f"⚠️ Churn Risk: **{churn_risk}**")
                else:
                    st.success(f"✅ Churn Risk: **{churn_risk}**")

                if churn_prob is not None:
                    st.metric(label="Churn Probability", value=f"{churn_prob * 100:.1f}%")

            else:
                st.error(f"Server returned status code: {response.status_code}")
                st.code(response.text)

        except requests.exceptions.RequestException as err:
            st.error(f"Failed to reach FastAPI backend: {err}")