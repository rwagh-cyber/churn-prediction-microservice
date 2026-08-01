import mlflow
import mlflow.sklearn
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Set MLflow experiment name
mlflow.set_experiment("Customer_Churn_XGBoost")

# Synthetic dataset generation
np.random.seed(42)
n_samples = 2000
df = pd.DataFrame({
    'tenure_months': np.random.randint(1, 72, n_samples),
    'monthly_charges': np.random.uniform(20.0, 150.0, n_samples),
    'total_charges': np.random.uniform(100.0, 8000.0, n_samples),
    'num_support_tickets': np.random.randint(0, 10, n_samples),
    'contract_type': np.random.choice(['month-to-month', 'one-year', 'two-year'], n_samples),
    'payment_method': np.random.choice(['electronic_check', 'credit_card', 'bank_transfer'], n_samples),
    'tech_support': np.random.choice(['yes', 'no'], n_samples)
})

churn_prob = ((df['num_support_tickets'] * 0.1) + (df['contract_type'] == 'month-to-month') * 0.25 - (df['tenure_months'] / 72 * 0.3))
df['churn'] = (churn_prob > 0.35).astype(int)

X = df.drop('churn', axis=1)
y = df['churn']

num_features = ['tenure_months', 'monthly_charges', 'total_charges', 'num_support_tickets']
cat_features = ['contract_type', 'payment_method', 'tech_support']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_features),
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
])

# Hyperparameters
params = {
    "n_estimators": 120,
    "max_depth": 5,
    "learning_rate": 0.03,
    "eval_metric": "logloss"
}

# Start MLflow Tracking
with mlflow.start_run():
    # 1. Log Hyperparameters
    mlflow.log_params(params)
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(**params))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    
    preds = pipeline.predict(X_test)
    probas = pipeline.predict_proba(X_test)[:, 1]
    
    # 2. Calculate & Log Metrics
    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, probas)
    f1 = f1_score(y_test, preds)
    
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("roc_auc", auc)
    mlflow.log_metric("f1_score", f1)
    
    # 3. Save Model Artifact
    joblib.dump(pipeline, 'churn_pipeline.joblib')
    mlflow.sklearn.log_model(pipeline, "model")
    
    print(f"Logged Run to MLflow. ROC-AUC: {auc:.4f}")