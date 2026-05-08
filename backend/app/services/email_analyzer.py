import re


def analyze_email(text: str):
    text_lower = text.lower()

    reasons = []
    score = 0

    urgent_words = [
        "urgent", "immediately", "now", "limited time",
        "account locked", "suspended", "verify now"
    ]

    phishing_keywords = [
        "verify", "password", "login", "bank",
        "credit card", "otp", "security alert"
    ]

    sensitive_requests = [
        "send your password",
        "enter your password",
        "confirm your password",
        "provide your otp",
        "enter your otp",
        "credit card number"
    ]

    suspicious_links = re.findall(r"http[s]?://\S+", text_lower)

    if any(word in text_lower for word in urgent_words):
        reasons.append("Uses urgent or threatening language")
        score += 2

    if any(word in text_lower for word in phishing_keywords):
        reasons.append("Contains phishing-related keywords")
        score += 1

    if any(phrase in text_lower for phrase in sensitive_requests):
        reasons.append("Requests sensitive information")
        score += 3

    if suspicious_links:
        reasons.append("Contains external links")
        score += 1

    if re.search(r"\bfree\b|\bprize\b|\bwinner\b|\breward\b", text_lower):
        reasons.append("Uses reward or prize language")
        score += 1

    if len(text.strip()) < 20:
        reasons.append("Email content is too short to fully trust")
        score += 1

    if score <= 1:
        risk_level = "Low"
        recommendation = "The email does not show strong phishing indicators, but still verify the sender."
    elif score <= 3:
        risk_level = "Medium"
        recommendation = "Be careful. Do not click links before verifying the sender and domain."
    else:
        risk_level = "High"
        recommendation = "Do not click links or share sensitive information. Report or delete the email."

    return {
        "risk_level": risk_level,
        "score": score,
        "reasons": reasons,
        "recommendation": recommendation
    }