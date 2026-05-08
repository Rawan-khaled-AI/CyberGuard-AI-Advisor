from fastapi import APIRouter
from pydantic import BaseModel

from app.services.url_analyzer import analyze_url
from app.ml.url_classifier import predict_url_risk
from app.services.risk_service import combine_url_risk

router = APIRouter()


class UrlRequest(BaseModel):
    url: str


@router.post("/analyze")
def analyze(data: UrlRequest):
    rule_result = analyze_url(data.url)
    model_result = predict_url_risk(data.url)
    final_decision = combine_url_risk(rule_result, model_result)

    return {
        "input": data.url,
        "rule_based_analysis": rule_result,
        "ml_model_analysis": model_result,
        "final_decision": final_decision,
    }