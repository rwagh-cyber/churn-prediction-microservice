import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

print("1. Generating Realistic Telecom Dataset...")
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

# Define churn logic based on features
churn_prob = (
    (df['num_support_tickets'] * 0.1) +
    (df['contract_type'] == 'month-to-month') * 0.25 +
    (df['monthly_charges'] / 150 * 0.2) -
    (df['tenure_months'] / 72 * 0.3)
)
df['churn'] = (churn_prob > 0.35).astype(int)

X = df.drop('churn', axis=1)
y = df['churn']

print("2. Building ColumnTransformer Preprocessing...")
num_features = ['tenure_months', 'monthly_charges', 'total_charges', 'num_support_tickets']
cat_features = ['contract_type', 'payment_method', 'tech_support']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
    ]
)

print("3. Assembling Full ML Pipeline...")
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, eval_metric='logloss'))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Model Evaluation
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
print(classification_report(y_test, y_pred))

print("4. Saving Complete Pipeline artifact...")
joblib.dump(pipeline, 'churn_pipeline.joblib')
print("Pipeline saved successfully as 'churn_pipeline.joblib'")