import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("1. Generating Synthetic Telecom Dataset...")
np.random.seed(42)
n_samples = 1000

# Generating features mimicking a telecom dataset
data = {
    'tenure_months': np.random.randint(1, 72, n_samples),
    'monthly_charges': np.random.uniform(20.0, 120.0, n_samples),
    'num_support_tickets': np.random.randint(0, 5, n_samples),
    'is_contract_month_to_month': np.random.randint(0, 2, n_samples)
}
df = pd.DataFrame(data)

# Generating target variable (Churn) based on features
churn_prob = (
    (df['num_support_tickets'] * 0.15) + 
    (df['is_contract_month_to_month'] * 0.3) + 
    (df['monthly_charges'] / 120 * 0.2) - 
    (df['tenure_months'] / 72 * 0.3)
)
df['churn'] = (churn_prob > 0.4).astype(int)

X = df.drop('churn', axis=1)
y = df['churn']

print("2. Training XGBoost Model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBClassifier(eval_metric='logloss', random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, preds):.2f}")

print("3. Saving Model File...")
with open('xgboost_churn_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved successfully as 'xgboost_churn_model.pkl'")