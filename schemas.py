from pydantic import BaseModel, Field
from typing import List, Literal

class CustomerInput(BaseModel):
    tenure_months: int = Field(..., ge=0, le=120, description="Tenure in months", examples=[12])
    monthly_charges: float = Field(..., ge=0.0, description="Monthly recurring charge in USD", examples=[85.50])
    total_charges: float = Field(..., ge=0.0, description="Lifetime charges in USD", examples=[1026.00])
    num_support_tickets: int = Field(..., ge=0, le=20, description="Number of customer support tickets raised", examples=[2])
    contract_type: Literal['month-to-month', 'one-year', 'two-year'] = Field(..., examples=['month-to-month'])
    payment_method: Literal['electronic_check', 'credit_card', 'bank_transfer'] = Field(..., examples=['electronic_check'])
    tech_support: Literal['yes', 'no'] = Field(..., examples=['no'])

class BatchCustomerInput(BaseModel):
    customers: List[CustomerInput]

class PredictionResponse(BaseModel):
    churn_prediction: int
    churn_probability: float
    churn_risk_level: str

# Compatibility aliases
CustomerData = CustomerInput