import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Prediction", page_icon="🚀", layout="wide")

st.title("📊 Customer Churn Prediction Dashboard")
st.write("Fill in customer details below to estimate churn risk.")

# --- UI Input Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    tenure_months = st.number_input("Tenure (Months)", min_value=0, value=12)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=65.50)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=786.00)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with col2:
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

with col3:
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior_citizen = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    num_support_tickets = st.number_input("Num Support Tickets", min_value=0, value=1)

# --- Predict Button ---
if st.button("🚀 Predict Churn Risk"):
    BACKEND_URL = "https://churn-prediction-microservice-3.onrender.com/predict/"

    # COMBINED PAYLOAD: Both Pydantic requirements + ML Model requirements
    payload = {
        # 1. Required by Pydantic Schema
        "MonthlyCharges": float(monthly_charges),
        "TotalCharges": float(total_charges),
        "Contract": contract,
        "OnlineSecurity": online_security,
        "TechSupport": tech_support,
        "PaperlessBilling": paperless_billing,
        "Gender": gender,
        "SeniorCitizen": int(senior_citizen),
        "Partner": partner,
        "Dependents": dependents,
        
        # 2. Required by ML Model Pipeline inside FastAPI
        "tenure_months": int(tenure_months),
        "monthly_charges": float(monthly_charges),
        "total_charges": float(total_charges),
        "contract_type": contract,
        "tech_support": tech_support,
        "payment_method": payment_method,
        "num_support_tickets": int(num_support_tickets)
    }

    with st.spinner("Connecting to FastAPI backend..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=30)

            if response.status_code == 200:
                res = response.json()
                
                prediction = res.get("prediction") or res.get("predict") or res.get("churn")
                churn_risk = res.get("churn_risk") or res.get("risk") or ("High" if prediction == 1 else "Low")
                churn_prob = res.get("churn_probability") or res.get("probability") or res.get("prob")

                st.subheader("Prediction Result:")
                if churn_risk == "High" or prediction == 1:
                    st.error(f"⚠️ Churn Risk: **{churn_risk}**")
                else:
                    st.success(f"✅ Churn Risk: **{churn_risk}**")

                if churn_prob is not None:
                    st.metric(label="Churn Probability", value=f"{churn_prob * 100:.1f}%")
                
                st.write("Full API Response:", res)

            else:
                st.error(f"Server returned status code: {response.status_code}")
                st.code(response.text)

        except requests.exceptions.RequestException as err:
            st.error(f"Failed to reach FastAPI backend: {err}")