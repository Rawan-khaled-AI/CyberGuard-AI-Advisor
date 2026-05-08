def combine_url_risk(rule_result: dict, model_result: dict) -> dict:
    rule_level = rule_result.get("risk_level", "Low")
    phishing_confidence = model_result.get("phishing_confidence", 0)

    final_score = 0
    reasons = []

    if rule_level == "Medium":
        final_score += 2
        reasons.append("Rule-based analysis detected medium risk signals.")
    elif rule_level == "High":
        final_score += 3
        reasons.append("Rule-based analysis detected high risk signals.")

    if phishing_confidence >= 0.8:
        final_score += 3
        reasons.append("Machine learning model strongly predicts phishing.")
    elif phishing_confidence >= 0.6:
        final_score += 2
        reasons.append("Machine learning model predicts possible phishing.")
    elif phishing_confidence >= 0.4:
        final_score += 1
        reasons.append("Machine learning model shows weak phishing probability.")

    if final_score >= 5:
        final_risk = "High"
        recommendation = "Do not open this URL. It is likely malicious."
    elif final_score >= 3:
        final_risk = "Medium"
        recommendation = "Be careful. Verify the URL before opening it."
    else:
        final_risk = "Low"
        recommendation = "The URL appears low risk, but still verify the source."

    return {
        "final_risk": final_risk,
        "final_score": final_score,
        "decision_reasons": reasons,
        "recommendation": recommendation,
    }
    
def combine_email_risk(rule_result: dict, model_result: dict) -> dict:
    rule_level = rule_result.get("risk_level", "Low")
    rule_reasons = rule_result.get("reasons", [])

    prediction = model_result.get("prediction", "")
    phishing_confidence = model_result.get("phishing_confidence", 0)

    final_score = 0
    reasons = []

    if rule_level == "Medium":
        final_score += 2
        reasons.append("Rule-based analysis detected medium phishing signals.")
    elif rule_level == "High":
        final_score += 3
        reasons.append("Rule-based analysis detected high phishing signals.")

    if prediction == "Phishing Email":
        if phishing_confidence >= 0.9:
            final_score += 4
            reasons.append("AI model strongly predicts phishing.")
        elif phishing_confidence >= 0.7:
            final_score += 3
            reasons.append("AI model predicts phishing with high confidence.")
        elif phishing_confidence >= 0.5:
            final_score += 2
            reasons.append("AI model predicts possible phishing.")
    else:
        reasons.append("AI model predicts the email is likely safe.")

    if "Requests sensitive information" in rule_reasons:
        final_score += 2
        reasons.append("Email requests sensitive information.")

    if "Contains external links" in rule_reasons:
        final_score += 1
        reasons.append("Email contains external links.")

    if "Uses urgent or threatening language" in rule_reasons:
        final_score += 1
        reasons.append("Email uses urgency or threatening language.")

    if final_score >= 6:
        final_risk = "High"
        recommendation = "Do not click links or share any sensitive information. Report or delete this email."
    elif final_score >= 3:
        final_risk = "Medium"
        recommendation = "Be careful. Verify the sender and links before taking action."
    else:
        final_risk = "Low"
        recommendation = "The email appears low risk, but still verify unexpected messages."

    return {
        "final_risk": final_risk,
        "final_score": final_score,
        "decision_reasons": reasons,
        "recommendation": recommendation,
    }