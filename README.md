````md
# CyberGuard AI Advisor

CyberGuard AI Advisor is a full-stack AI-powered cybersecurity assistant designed to help users detect phishing emails, analyze suspicious URLs, respond to security incidents, and receive defensive cybersecurity guidance in Arabic and English.

The project is built as a production-style AI system, not just a simple chatbot. It combines rule-based analysis, machine learning models, Retrieval-Augmented Generation (RAG), LLM reasoning, PostgreSQL conversation memory, and a modern React chat interface.

---

## Live Demo

Frontend:  
https://cyber-guard-ai-advisor.vercel.app

Backend API:  
https://cyberguard-ai-advisor-production.up.railway.app

API Docs:  
https://cyberguard-ai-advisor-production.up.railway.app/docs

---

## Main Features

- Conversational cybersecurity assistant
- Phishing email analysis
- Suspicious URL risk analysis
- Incident response guidance
- Arabic and English support
- Rule-based security analysis
- ML-based phishing email detection
- ML-based URL risk detection
- RAG pipeline using FAISS and sentence-transformers
- OpenRouter LLM integration
- PostgreSQL conversation memory
- Chat history persistence
- Safety layer against offensive cybersecurity misuse
- FastAPI backend
- React + Vite frontend
- Dockerized backend
- Cloud deployment using Railway, Vercel, and Neon
- Hugging Face model hosting

---

# System Architecture

```text
User
 |
 v
React Frontend (Vercel)
 |
 v
FastAPI Backend (Railway)
 |
 |-- Chat API
 |-- Email Analysis API
 |-- URL Analysis API
 |-- Password Safety API
 |-- Reports API
 |
 |-- Rule-Based Analyzers
 |-- ML Models
 |     |-- Email Phishing Model from Hugging Face
 |     |-- URL Risk Model from Hugging Face
 |
 |-- RAG Pipeline
 |     |-- Knowledge Base
 |     |-- Sentence Transformers
 |     |-- FAISS Vector Store
 |     |-- OpenRouter LLM
 |
 v
PostgreSQL Database (Neon)
 |
 |-- Chat Sessions
 |-- Chat Messages
 |-- Security Events
 
````

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* FAISS
* sentence-transformers
* Transformers
* scikit-learn
* Hugging Face Hub
* OpenRouter API
* Docker

## Frontend

* React
* Vite
* Axios
* Lucide React
* CSS

## Deployment

* Railway for backend
* Vercel for frontend
* Neon PostgreSQL for database
* Hugging Face Hub for ML model hosting

---

# Project Structure

```text
CyberGuard-AI-Advisor/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── rag_pipeline.py
│   │   │
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── v1/
│   │   │       ├── chat.py
│   │   │       ├── email.py
│   │   │       ├── password.py
│   │   │       ├── reports.py
│   │   │       └── url.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   │
│   │   ├── knowledge_base/
│   │   │   └── cyber_kb.md
│   │   │
│   │   ├── ml/
│   │   │   ├── email_classifier.py
│   │   │   ├── url_classifier.py
│   │   │   ├── url_feature_extractor.py
│   │   │   ├── train_email_model.py
│   │   │   └── train_url_model.py
│   │   │
│   │   ├── models/
│   │   │   ├── chat.py
│   │   │   └── security_event.py
│   │   │
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   ├── email_analyzer.py
│   │   │   ├── memory_service.py
│   │   │   ├── risk_service.py
│   │   │   └── url_analyzer.py
│   │   │
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# How the Chat Pipeline Works

When a user sends a message:

1. The React frontend sends the message to the FastAPI backend.
2. The backend creates or resumes a chat session.
3. The user message is saved to PostgreSQL.
4. The system checks the message type:

   * URL analysis
   * Email phishing analysis
   * Incident response
   * General cybersecurity question
5. The correct pipeline is selected:

   * Rule-based analyzer
   * ML classifier
   * RAG pipeline
   * LLM response
6. The assistant response is saved to PostgreSQL.
7. The final response is returned to the frontend.

---

# Machine Learning Models

## Email Phishing Model

The email phishing detector is based on a fine-tuned DistilBERT model.

The trained model is hosted on Hugging Face Hub:

```text
rawankhaled46/cyberguard-email-phishing-model
```

This allows the backend to load the model directly during deployment without storing large model files inside the GitHub repository.

## URL Risk Model

The URL risk detector is a scikit-learn model saved as a `.pkl` file and hosted on Hugging Face Hub:

```text
rawankhaled46/cyberguard-url-model
```

The model is downloaded at runtime using `huggingface_hub`.

---

# RAG Pipeline

CyberGuard uses Retrieval-Augmented Generation to answer cybersecurity questions using a curated knowledge base.

The RAG flow:

```text
User Question
   ↓
Text Embedding
   ↓
FAISS Similarity Search
   ↓
Relevant Cybersecurity Context
   ↓
OpenRouter LLM
   ↓
Final Defensive Security Answer
```

The knowledge base contains defensive cybersecurity content, incident response steps, phishing awareness, password safety, suspicious URL guidance, and security best practices.

---

# Safety Layer

CyberGuard includes a safety layer to prevent offensive cybersecurity misuse.

The assistant refuses requests related to:

* Hacking instructions
* Password stealing
* Malware creation
* Exploit development
* Phishing kits
* Bypassing security systems

Instead, it redirects the user toward defensive guidance, prevention, detection, and safe security practices.

---

# Environment Variables

Create a `.env` file inside the `backend` directory:

```env
DATABASE_URL=postgresql://username:password@host/database?sslmode=require
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

Never commit `.env` files to GitHub.

---

# Running the Backend Locally

Go to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

# Running the Frontend Locally

Go to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

---

# Running with Docker

From the backend directory:

```bash
docker build -t cyberguard-backend .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env cyberguard-backend
```

---

# Database Migrations

Alembic is used for managing database schema changes.

Create a new migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

In production, migrations are executed before starting the backend container.

---

# Deployment

## Backend

The backend is deployed on Railway using Docker.

Railway runs:

```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Database

PostgreSQL is hosted on Neon.

## Frontend

The React frontend is deployed on Vercel.

## Models

ML models are hosted on Hugging Face Hub.

---

# API Endpoints

## Chat

```http
POST /chat/
```

Request:

```json
{
  "message": "I clicked a suspicious link, what should I do?"
}
```

Response:

```json
{
  "session_id": "session-id",
  "response": {
    "type": "rag_cyber_advice",
    "answer": "..."
  }
}
```

## Get Chat History

```http
GET /chat/{session_id}
```

## URL Analysis

```http
POST /url/analyze
```

## Email Analysis

```http
POST /email/analyze
```

## Password Check

```http
POST /password/check
```

---

# Engineering Decisions

## Why PostgreSQL instead of SQLite?

PostgreSQL was chosen because the project needs persistent conversation history, production-style deployment, reliable schema migrations, and scalability.

## Why Docker?

Docker ensures the backend runs consistently across local development and cloud deployment.

## Why Railway for backend?

Railway supports Docker-based FastAPI deployment and is suitable for backend services that require long-running APIs.

## Why Vercel for frontend?

Vercel is optimized for React/Vite frontend deployment and provides fast CDN-based hosting.

## Why Neon?

Neon provides managed PostgreSQL with a free tier, SSL support, and easy integration with cloud backends.

## Why Hugging Face Hub?

Hugging Face Hub acts as a model registry. It keeps large ML artifacts outside the code repository and allows models to be loaded dynamically during deployment.

---

# Current Limitations

* Authentication is not implemented yet.
* Rate limiting is planned but not yet enabled.
* Some ML models may need further evaluation before production use.
* The system is focused on defensive cybersecurity guidance only.
* The chatbot should not be used as a replacement for professional incident response.

---

# Future Improvements

* User authentication
* User-specific chat history
* Security report export
* File upload for email analysis
* Better observability and logging
* Rate limiting
* Admin dashboard
* More advanced incident reports
* Model monitoring
* CI/CD testing pipeline
* Improved Arabic cybersecurity knowledge base
* Dedicated ML inference service

---

# Status

CyberGuard AI Advisor is currently deployed as a working full-stack AI cybersecurity assistant with:

* Live React frontend
* Live FastAPI backend
* PostgreSQL conversation memory
* RAG-based cybersecurity responses
* Hugging Face-hosted ML models
* Cloud deployment pipeline

---

# Author

Developed by Rawan Khaled.

GitHub:
[https://github.com/Rawan-khaled-AI](https://github.com/Rawan-khaled-AI)

```
```
