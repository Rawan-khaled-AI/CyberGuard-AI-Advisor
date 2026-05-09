from pathlib import Path
import os
import requests

import faiss
import torch
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

KB_PATH = Path("app/knowledge_base/cyber_kb.md")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")

device = "cuda" if torch.cuda.is_available() else "cpu"

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device=device,
)

chunks = []
index = None


def detect_language(text: str) -> str:
    arabic_chars = sum(1 for ch in text if "\u0600" <= ch <= "\u06ff")
    english_chars = sum(1 for ch in text if ch.isascii() and ch.isalpha())

    return "arabic" if arabic_chars > english_chars else "english"


def load_knowledge_base():
    global chunks, index

    text = KB_PATH.read_text(encoding="utf-8")
    raw_chunks = text.split("---")
    chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True,
    ).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    print(f"RAG loaded on device: {device}")
    print(f"Knowledge chunks loaded: {len(chunks)}")


def retrieve_context(question: str, top_k: int = 2) -> str:
    global index

    if index is None:
        load_knowledge_base()

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = []
    for idx in indices[0]:
        if 0 <= idx < len(chunks):
            retrieved_chunks.append(chunks[idx])

    return "\n\n".join(retrieved_chunks)


def is_unsafe_question(question: str) -> bool:
    lowered = question.lower()

    unsafe_keywords = [
        "hack",
        "steal password",
        "bypass",
        "crack",
        "exploit",
        "phishing kit",
        "ddos",
        "keylogger",
        "ransomware",
        "payload",
    ]

    return any(keyword in lowered for keyword in unsafe_keywords)


def build_prompt(question: str, context: str) -> str:
    user_language = detect_language(question)

    language_rule = (
        "The user wrote in Arabic. Reply ONLY in natural clear Arabic. Do not use English."
        if user_language == "arabic"
        else "The user wrote in English. Reply ONLY in English. Do not use Arabic."
    )

    return f"""
You are CyberGuard AI Advisor, a professional defensive cybersecurity assistant.

Critical language rule:
{language_rule}

Main goal:
Give short, practical, safe cybersecurity guidance like a real chat assistant.

Safety:
- Defensive cybersecurity only.
- Never tell the user to open, test, revisit, type, or click a suspicious link again.
- If the user clicked a suspicious link, give safe incident-response steps.
- Do not provide hacking, malware, bypassing, exploitation, credential theft, or harmful instructions.
- If the question is harmful, refuse briefly and redirect to safe protection advice.

Style:
- Do not repeat the user's question.
- Do not mention knowledge base, context, RAG, internal tools, or model.
- Do not use markdown symbols like ** or ###.
- Keep the answer compact.
- Use short paragraphs.
- Use numbered steps when giving actions.
- Avoid large empty spaces.
- Avoid unnecessary section titles.
- Sound practical, calm, and human.

Cybersecurity context:
{context}

User question:
{question}
"""


def generate_with_llm(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        return (
            "LLM API key is not configured. I retrieved the relevant cybersecurity context, "
            "but generation is disabled."
        )

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are CyberGuard AI Advisor. "
                    "Give safe, defensive cybersecurity guidance only. "
                    "You must answer only in the user's language."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.1,
        "max_tokens": 350,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"LLM generation failed: {str(e)}"


def clean_answer(answer: str) -> str:
    unwanted = [
        "Title:",
        "Quick Answer:",
        "Risk Indicators:",
        "Protection Steps:",
        "Final Advice:",
        "العنوان:",
        "الإجابة السريعة:",
        "العلامات المخاطر:",
        "المشورة النهائية:",
    ]

    for item in unwanted:
        answer = answer.replace(item, "")

    answer = (
        answer.replace("\\n", "\n")
        .replace("###", "")
        .replace("**", "")
        .replace("اقفز الانترنت", "افصل الإنترنت مؤقتًا")
        .replace("اقفز الإنترنت", "افصل الإنترنت مؤقتًا")
        .replace("ارفع الانترنت", "افصل الإنترنت مؤقتًا")
        .replace("ارفع الإنترنت", "افصل الإنترنت مؤقتًا")
        .strip()
    )

    lines = [line.strip() for line in answer.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)


def enforce_language(answer: str, question: str) -> str:
    language = detect_language(question)

    has_arabic = any("\u0600" <= ch <= "\u06ff" for ch in answer)
    has_english = any(ch.isascii() and ch.isalpha() for ch in answer)

    if language == "english" and has_arabic:
        answer = generate_with_llm(
            "Rewrite the following answer in English only. "
            "Do not add new information:\n\n"
            f"{answer}"
        )
        return clean_answer(answer)

    if language == "arabic" and has_english:
        answer = generate_with_llm(
            "أعد كتابة الإجابة التالية باللغة العربية فقط بدون إضافة معلومات جديدة:\n\n"
            f"{answer}"
        )
        return clean_answer(answer)

    return answer


def answer_with_rag(question: str) -> dict:
    if is_unsafe_question(question):
        return {
            "type": "safe_response",
            "answer": (
                "لا أقدر أساعد في أي استخدام هجومي أو ضار للأمن السيبراني. "
                "أقدر أساعدك في الحماية، التوعية، اكتشاف المخاطر، والاستجابة الآمنة للحوادث."
                if detect_language(question) == "arabic"
                else "I can’t help with harmful or offensive cybersecurity actions. "
                "I can help with defensive security, awareness, prevention, detection, and safe incident response."
            ),
            "device": device,
        }

    context = retrieve_context(question)
    prompt = build_prompt(question, context)
    answer = generate_with_llm(prompt)
    answer = clean_answer(answer)
    answer = enforce_language(answer, question)

    return {
        "type": "rag_cyber_advice",
        "answer": answer,
        "device": device,
        "model": OPENROUTER_MODEL,
    }
