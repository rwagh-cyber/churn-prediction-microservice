import streamlit as st
import requests

# Page Config (Title & Favicon)
st.set_page_config(
    page_title="Churn Predictor Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI Styling
st.markdown("""
    <style>
    /* Main App Background Gradient */
    .stApp {
        background: linear-gradient(to right, #0f172a, #1e293b);
        color: #f8fafc;
    }
    
    /* Card Container Styling */
    div[data-testid="stVerticalBlock"] > div {
        background-color: rgba(30, 41, 59, 0.7);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Custom Styling for Predict Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        font-weight: bold;
        font-size: 18px;
        padding: 12px;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        box-shadow: 0px 4px 15px rgba(59, 130, 246, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("📊 Customer Churn Analytics Dashboard")
st.caption("Predict customer retention risk in real-time using AI/ML microservices.")
st.divider()

# Layout: Sidebar for Customer Info, Main Area for Financials & Prediction
with st.sidebar:
    st.header("👤 Customer Profile")
    tenure = st.slider("Tenure (Months)", min_value=1, max_value=72, value=12)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    payment_method = st.selectbox("Payment Method", [
        "Electronic check", 
        "Mailed check", 
        "Bank transfer (automatic)", 
        "Credit card (automatic)"
    ])

# Main Area Inputs in 2 Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Financial Details")
    monthly_charges = st.number_input("Monthly Charges ($)", value=65.50, step=1.0)
    total_charges = st.number_input("Total Charges ($)", value=786.00, step=10.0)

with col2:
    st.subheader("🛠️ Service & Support")
    tech_support = st.selectbox("Tech Support Included?", ["No", "Yes", "No internet service"])
    num_support_tickets = st.number_input("Support Tickets Raised", min_value=0, max_value=20, value=1)

st.divider()

# Predict Button
if st.button("🚀 Run Prediction Analysis"):
    # Backend Payload
    # Corrected Payload for FastAPI
    payload = {
        "tenure_months": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract_type": contract,
        "payment_method": payment_method,
        "tech_support": tech_support,
        "num_support_tickets": num_support_tickets
    }
    
    # Backend URL
    BACKEND_URL = "https://churn-prediction-microservice-3.onrender.com/predict"
    
    with st.spinner("Analyzing risk factors..."):
        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                churn_risk = result.get("churn_risk", "Unknown")
                prob = result.get("churn_probability", 0) * 100
                
                st.subheader("📊 Prediction Results")
                m1, m2 = st.columns(2)
                
                if churn_risk == "High":
                    m1.error(f"🚨 **Churn Risk:** {churn_risk}")
                else:
                    m1.success(f"✅ **Churn Risk:** {churn_risk}")
                    
                m2.metric(label="Churn Probability", value=f"{prob:.1f}%")
                
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")