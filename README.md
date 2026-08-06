# 🚀 Enterprise Customer Churn Prediction & Monitoring Microservice

An enterprise-grade, end-to-end Machine Learning Microservice engineered with **FastAPI**, **XGBoost**, **Optuna**, and **Evidently AI**. This production pipeline delivers real-time low-latency inference, automated hyperparameter optimization, and continuous data drift monitoring. Containerized with **Docker** for seamless deployment.

---

## 🏗️ System Architecture

```text
               ┌──────────────────────────────────────────────┐
               │         FastAPI Production Gateway           │
               └──────────────────────┬───────────────────────┘
                                      │
           ┌──────────────────────────┴──────────────────────────┐
           ▼                                                     ▼
┌───────────────────────────────┐                     ┌────────────────────┐
│ XGBoost Model (Optuna-Tuned) │                     │ SQLite Audit Logger│
└──────────────┬────────────────┘                     └─────────┬──────────┘
               │                                                │
               ▼                                                ▼
┌───────────────────────────────┐                     ┌────────────────────┐
│ MLflow Experiment Artifacts   │                     │ Evidently AI Drift │
└───────────────────────────────┘                     └────────────────────┘
Key Features
⚡ Production API Gateway: High-performance RESTful API built with FastAPI supporting both single-instance and high-throughput batch inference.

🎯 Automated Hyperparameter Optimization: Integrated Optuna with 5-Fold Stratified Cross-Validation to automatically fine-tune XGBoost hyperparameters for optimal ROC-AUC score.

📊 Continuous Model & Data Drift Monitoring: Implemented Evidently AI to automatically monitor incoming inference payloads against baseline training distributions to detect feature drift.

🛡️ Strict Data Validation: Utilized Pydantic v2 schema validation to guarantee payload integrity and zero runtime data corruption.

📝 Audit & Compliance Logging: Automated SQLite tracking to log input payloads, prediction probabilities, and timestamped confidence scores.

🧪 Test-Driven Development (TDD): Full unit test coverage instrumented with PyTest for automated CI/CD validation.

🐳 Containerization: Fully containerized using Docker for reliable, cloud-ready deployment across any environment.

🛠️ Tech Stack
Language: Python 3.10+

Machine Learning & Tuning: XGBoost, Scikit-Learn, Optuna, MLflow

Model Monitoring: Evidently AI

API Framework: FastAPI, Uvicorn, Pydantic

Database & Storage: SQLite3, Joblib

Testing & Quality Assurance: PyTest

Deployment: Docker

📂 Project Structure
Plaintext
churn_project/
├── main.py                  # FastAPI Application Gateway & Drift Endpoints
├── tune_model.py            # Optuna Automated Hyperparameter Tuning Pipeline
├── churn_pipeline.joblib    # Trained & Optimized XGBoost Pipeline
├── tests/                   # PyTest Automated Unit Testing Suite
│   └── test_api.py
├── predictions_log.db       # SQLite Database for Inference Logging
├── Dockerfile               # Docker Image Configuration
├── .dockerignore            # Docker Build Exclusions
├── requirements.txt         # Project Dependencies
└── README.md                # Project Documentation
🐳 Running with Docker (Recommended)
The easiest way to run this microservice is via Docker.

1. Build the Docker Image
Bash
docker build -t churn-prediction-api .
2. Launch the Container
Bash
docker run -p 8000:8000 churn-prediction-api
Access the Interactive Swagger Documentation at: http://localhost:8000/docs

⚡ Quickstart & Local Installation (Without Docker)
1. Clone the Repository
Bash
git clone [https://github.com/YOUR_USERNAME/churn-prediction-microservice.git](https://github.com/YOUR_USERNAME/churn-prediction-microservice.git)
cd churn-prediction-microservice
2. Set Up Virtual Environment & Install Dependencies
Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
3. Run Hyperparameter Tuning Pipeline
Optimize the XGBoost pipeline using Optuna and save the optimized artifact:

Bash
python tune_model.py
4. Launch Production Server
Bash
uvicorn main:app --reload
🌐 API & Dashboard Endpoints
Once the application is running, open your browser to access the interactive interfaces:

Interactive Swagger UI: http://127.0.0.1:8000/docs

Health Check: http://127.0.0.1:8000/health

Data Drift Visual Dashboard: http://127.0.0.1:8000/monitoring/drift

🧪 Running Automated Tests
Run the full unit and API integration test suite using PyTest:

Bash
pytest
