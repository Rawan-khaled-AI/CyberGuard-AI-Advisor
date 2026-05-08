import re
from urllib.parse import urlparse

def analyze_url(url: str):
    reasons = []
    score = 0

    parsed = urlparse(url)

    # 1. HTTPS check
    if parsed.scheme != "https":
        reasons.append("Not using HTTPS")
        score += 1

    # 2. suspicious keywords
    suspicious_keywords = ["login", "secure", "update", "bank", "verify"]

    if any(word in url.lower() for word in suspicious_keywords):
        reasons.append("Contains suspicious keywords")
        score += 1

    # 3. domain length
    if len(parsed.netloc) > 25:
        reasons.append("Unusually long domain")
        score += 1

    # 4. numbers in domain
    if re.search(r"\d", parsed.netloc):
        reasons.append("Domain contains numbers")
        score += 1

    # risk level
    if score == 0:
        risk = "Low"
    elif score <= 2:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "risk_level": risk,
        "score": score,
        "reasons": reasons
    }