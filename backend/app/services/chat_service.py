import re

from app.services.email_analyzer import analyze_email
from app.ml.email_classifier import predict_email_phishing
from app.services.url_analyzer import analyze_url
from app.ml.url_classifier import predict_url_risk
from app.services.risk_service import combine_email_risk, combine_url_risk
from app.ai.rag_pipeline import answer_with_rag


def extract_url(text: str) -> str | None:
    match = re.search(r"https?://[^\s]+", text)
    return match.group(0) if match else None


def is_email_analysis_request(text: str) -> bool:
    lowered = text.lower()

    email_signals = [
        "email",
        "message",
        "inbox",
        "account suspended",
        "verify your password",
        "urgent",
        "click",
        "otp",
        "bank account",
    ]

    return any(signal in lowered for signal in email_signals)


def build_contextual_message(message: str, conversation_context: str | None = None) -> str:
    if not conversation_context:
        return message

    return (
        "Previous conversation context:\n"
        f"{conversation_context}\n\n"
        "Current user message:\n"
        f"{message}"
    )


def answer_general_cyber_question(question: str) -> dict:
    lowered = question.lower()

    unsafe_keywords = [
        "hack",
        "steal password",
        "bypass",
        "crack",
        "exploit",
        "malware",
        "phishing kit",
    ]

    if any(word in lowered for word in unsafe_keywords):
        return {
            "type": "safe_response",
            "answer": (
                "I can’t help with offensive or harmful cybersecurity actions. "
                "I can help you understand defensive security, prevention, detection, "
                "and how to protect systems safely."
            ),
        }

    if "phishing" in lowered:
        answer = (
            "Phishing is a social engineering attack where attackers try to trick users "
            "into clicking malicious links or sharing sensitive information such as passwords, "
            "OTP codes, or banking details. To stay safe, verify the sender, avoid clicking "
            "unknown links, and never share credentials through email."
        )
    elif "password" in lowered:
        answer = (
            "A strong password should be long, unique, and hard to guess. Use at least "
            "12 characters with uppercase, lowercase, numbers, and symbols. Avoid reusing "
            "passwords and enable multi-factor authentication."
        )
    elif "url" in lowered or "link" in lowered:
        answer = (
            "To check a suspicious link, look for HTTPS, unusual domains, misspellings, "
            "shortened URLs, suspicious words like login or verify, and unfamiliar top-level "
            "domains such as .xyz or .tk."
        )
    else:
        answer = (
            "I can help with cybersecurity awareness, phishing detection, suspicious URLs, "
            "password safety, and defensive recommendations. Please describe the security "
            "problem or paste the email/link you want to analyze."
        )

    return {
        "type": "general_cyber_advice",
        "answer": answer,
    }


def handle_chat_message(
    message: str,
    conversation_context: str | None = None,
) -> dict:
    lowered = message.lower()
    url = extract_url(message)

    contextual_message = build_contextual_message(
        message=message,
        conversation_context=conversation_context,
    )

    if url:
        rule_result = analyze_url(url)
        model_result = predict_url_risk(url)
        final_decision = combine_url_risk(rule_result, model_result)

        return {
            "type": "url_analysis",
            "detected_url": url,
            "rule_based_analysis": rule_result,
            "ml_model_analysis": model_result,
            "final_decision": final_decision,
            "assistant_reply": (
                f"I analyzed the URL and classified it as {final_decision['final_risk']} risk. "
                f"Recommendation: {final_decision['recommendation']}"
            ),
        }

    incident_signals = [
        "i clicked",
        "clicked a suspicious link",
        "clicked suspicious link",
        "opened a suspicious link",
        "opened suspicious link",
        "suspicious link",
        "what should i do now",
        "entered my password",
        "typed my password",
        "shared my password",
        "دخلت الباسورد",
        "كتبت الباسورد",
        "ضغطت على لينك",
        "لينك مشبوه",
    ]

    if any(signal in lowered for signal in incident_signals):
        result = answer_with_rag(contextual_message)
        result["priority"] = "incident_response"
        return result

    if is_email_analysis_request(message):
        rule_result = analyze_email(message)
        model_result = predict_email_phishing(message)
        final_decision = combine_email_risk(rule_result, model_result)

        return {
            "type": "email_analysis",
            "rule_based_analysis": rule_result,
            "ml_model_analysis": model_result,
            "final_decision": final_decision,
            "assistant_reply": (
                f"I analyzed the email and classified it as {final_decision['final_risk']} risk. "
                f"Recommendation: {final_decision['recommendation']}"
            ),
        }

    return answer_with_rag(contextual_message)