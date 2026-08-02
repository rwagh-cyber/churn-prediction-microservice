import streamlit as st
import requests

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Enterprise Customer Churn Prediction Dashboard")
st.write("Enter customer details below to predict churn probability in real-time.")

# Form Layout
with st.form("churn_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=120, value=12)
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=65.5)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=786.0)
        contract = st.selectbox("Contract Type", ["month-to-month", "one-year", "two-year"])
        
    with col2:
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["yes", "no"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        
    with col3:
        payment_method_display = st.selectbox("Payment Method", [
            "Electronic Check", 
            "Credit Card", 
            "Bank Transfer"
        ])
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])

    submit_button = st.form_submit_button("🚀 Predict Churn Risk")

if submit_button:
    # Map payment method display name to backend expected enum
    payment_map = {
        "Electronic Check": "electronic_check",
        "Credit Card": "credit_card",
        "Bank Transfer": "bank_transfer"
    }
    payment_method = payment_map[payment_method_display]

    # Payload matching FastAPI Pydantic Schema exactly
    payload = {
        "tenure_months": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract_type": contract,
        "num_support_tickets": 1,
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "tech_support": tech_support,
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "PaperlessBilling": paperless_billing,
        "payment_method": payment_method
    }

    try:
        # Send payload to local FastAPI server
# Send payload to Render FastAPI backend server
        response = requests.post("https://churn-prediction-microservice-1.onrender.com/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            churn_prob = result.get("churn_probability", result.get("probability", 0.0))
            is_churn = result.get("churn_prediction", result.get("prediction", 0))

            st.markdown("---")
            st.subheader("🎯 Prediction Result")
            
            if is_churn == 1 or churn_prob > 0.5:
                st.error(f"⚠️ **High Churn Risk!** Customer is likely to leave. Risk Probability: **{churn_prob*100:.1f}%**")
            else:
                st.success(f"✅ **Low Churn Risk.** Customer is likely to stay. Retention Confidence: **{(1-churn_prob)*100:.1f}%**")
        else:
            st.warning(f"FastAPI Server returned status code: {response.status_code}")
            st.write(response.text)
            
    except Exception as e:
        st.error("❌ Could not connect to FastAPI Backend. Make sure `uvicorn main:app` is running!")