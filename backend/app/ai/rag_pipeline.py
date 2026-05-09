from pathlib import Path
import os
import requests

import faiss
import numpy as np
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
    return f"""
You are CyberGuard AI Advisor, a professional defensive cybersecurity assistant.

Main goal:
Give short, practical, safe cybersecurity guidance like a real chat assistant.

Language:
- VERY IMPORTANT:
- Detect the language of the user's message.
- Reply ONLY in that same language.
- If the user writes Arabic, answer ONLY in Arabic.
- If the user writes English, answer ONLY in English.
- Never switch languages.
- Never translate unless the user asks.
- Never mix Arabic and English unless the user mixes them first.

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

Arabic style:
- Use natural Arabic.
- Avoid awkward phrases.
- Say "افصل الإنترنت مؤقتًا" not "ارفع الإنترنت" or "اقفز الإنترنت".
- Say "نصيحة أخيرة" if needed.
- Say "مؤشرات الخطر" if needed.

Cybersecurity context:
{context}

User question:
{question}

For incident response questions like clicking a suspicious link, answer like this style:
ضغطك على لينك مشبوه ممكن يعرّض بياناتك أو جهازك للخطر، لكن تقدر تقلل الضرر بسرعة لو اتصرفت صح:

1. متفتحش اللينك تاني.
2. لو دخلت باسورد أو حمّلت ملف، افصل الإنترنت مؤقتًا.
3. غيّر كلمات المرور المهمة من جهاز موثوق.
4. فعّل المصادقة متعددة العوامل MFA.
5. اعمل فحص كامل للجهاز ببرنامج حماية موثوق.
6. لو دخلت بيانات بنكية أو بيانات حساب، تواصل مع البنك أو الدعم فورًا.

For general protection questions, answer with:
- brief explanation
- 3 to 5 practical steps
- one final short advice
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
                    "Keep answers compact, practical, and in the user's language."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
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


def answer_with_rag(question: str) -> dict:
    if is_unsafe_question(question):
        return {
            "type": "safe_response",
            "answer": (
                "لا أقدر أساعد في أي استخدام هجومي أو ضار للأمن السيبراني. "
                "أقدر أساعدك في الحماية، التوعية، اكتشاف المخاطر، والاستجابة الآمنة للحوادث."
                if any("\u0600" <= ch <= "\u06FF" for ch in question)
                else
                "I can’t help with harmful or offensive cybersecurity actions. "
                "I can help with defensive security, awareness, prevention, detection, and safe incident response."
            ),
            "device": device,
        }

    context = retrieve_context(question)
    prompt = build_prompt(question, context)
    answer = generate_with_llm(prompt)
    answer = clean_answer(answer)

    return {
        "type": "rag_cyber_advice",
        "answer": answer,
        "device": device,
        "model": OPENROUTER_MODEL,
    }