import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Prediction", page_icon="🚀", layout="wide")

st.title("📊 Customer Churn Prediction Dashboard")
st.write("Fill in customer details below to estimate churn risk.")

# --- UI Input Layout ---
col1, col2 = st.columns(2)

with col1:
    tenure_months = st.number_input("Tenure (Months)", min_value=0, max_value=120, value=12)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=85.50)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=1026.00)
    num_support_tickets = st.number_input("Support Tickets Raised", min_value=0, max_value=20, value=2)

with col2:
    contract_type = st.selectbox(
        "Contract Type", 
        options=["month-to-month", "one-year", "two-year"]
    )
    
    payment_method = st.selectbox(
        "Payment Method", 
        options=["electronic_check", "credit_card", "bank_transfer"]
    )
    
    tech_support = st.selectbox(
        "Tech Support", 
        options=["yes", "no"]
    )

# --- Predict Action ---
if st.button("🚀 Predict Churn Risk"):
    # URL चा शेवटी trailing slash (/) जोडला आहे ज्यामुळे 405 Redirect एरर येणार नाही
    BACKEND_URL = "https://churn-prediction-microservice-3.onrender.com/predict/"

    payload = {
        "tenure_months": int(tenure_months),
        "monthly_charges": float(monthly_charges),
        "total_charges": float(total_charges),
        "num_support_tickets": int(num_support_tickets),
        "contract_type": contract_type,
        "payment_method": payment_method,
        "tech_support": tech_support
    }

    with st.spinner("Connecting to FastAPI backend..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=30)

            if response.status_code == 200:
                res = response.json()
                
                churn_pred = res.get("churn_prediction")
                churn_prob = res.get("churn_probability", 0.0)
                risk_level = res.get("churn_risk_level", "Unknown")

                st.subheader("Prediction Result:")
                if churn_pred == 1 or str(risk_level).lower() == "high":
                    st.error(f"⚠️ Churn Risk Level: **{risk_level}**")
                else:
                    st.success(f"✅ Churn Risk Level: **{risk_level}**")

                st.metric(label="Churn Probability", value=f"{churn_prob * 100:.1f}%")

            else:
                st.error(f"FastAPI Server returned status code: {response.status_code}")
                st.code(response.text)

        except requests.exceptions.RequestException as err:
            st.error(f"Failed to reach FastAPI backend: {err}")