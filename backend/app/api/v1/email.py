from fastapi import APIRouter
from pydantic import BaseModel

from app.services.email_analyzer import analyze_email
from app.ml.email_classifier import predict_email_phishing
from app.services.risk_service import combine_email_risk

router = APIRouter()


class EmailRequest(BaseModel):
    text: str


@router.post("/analyze")
def analyze(data: EmailRequest):
    rule_result = analyze_email(data.text)
    model_result = predict_email_phishing(data.text)
    final_decision = combine_email_risk(rule_result, model_result)

    return {
        "input": data.text,
        "rule_based_analysis": rule_result,
        "ml_model_analysis": model_result,
        "final_decision": final_decision,
    }