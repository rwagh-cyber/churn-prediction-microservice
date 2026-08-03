import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Prediction", page_icon="🚀", layout="wide")

st.title("📊 Customer Churn Prediction Dashboard")
st.write("Fill in customer details below to estimate churn risk.")

st.markdown("---")

# --- UI Input Layout ---
col1, col2 = st.columns(2)

with col1:
    tenure_months = st.number_input("Tenure (Months)", min_value=0, value=12)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=65.50)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=786.00)
    contract_type = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with col2:
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    num_support_tickets = st.number_input("Num Support Tickets", min_value=0, value=1)

st.markdown("---")

# --- Predict Button ---
if st.button("🚀 Predict Churn Risk", use_container_width=True):
    # Live FastAPI Backend Endpoint
    BACKEND_URL = "https://churn-prediction-microservice-3.onrender.com/predict/"

    # Sending exact 7 features required by FastAPI and ML pipeline
    payload = {
        "tenure_months": int(tenure_months),
        "monthly_charges": float(monthly_charges),
        "total_charges": float(total_charges),
        "contract_type": contract_type,
        "tech_support": tech_support,
        "payment_method": payment_method,
        "num_support_tickets": int(num_support_tickets)
    }

    with st.spinner("Connecting to Backend Service..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=30)

            if response.status_code == 200:
                res = response.json()
                
                prediction = res.get("prediction")
                churn_risk = res.get("churn_risk", "Unknown")
                churn_prob = res.get("churn_probability")

                st.subheader("🎯 Prediction Result:")
                
                if churn_risk == "High" or prediction == 1:
                    st.error(f"⚠️ Churn Risk: **{churn_risk}**")
                else:
                    st.success(f"✅ Churn Risk: **{churn_risk}**")

                if churn_prob is not None:
                    st.metric(label="Churn Probability", value=f"{churn_prob * 100:.1f}%")

            else:
                st.error(f"Server Error (Status Code {response.status_code}):")
                st.code(response.text)

        except requests.exceptions.RequestException as err:
            st.error(f"Failed to connect to backend service: {err}")