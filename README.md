# CyberGuard AI Advisor

CyberGuard AI Advisor is a full-stack AI-powered cybersecurity assistant designed to help users detect phishing emails, analyze suspicious URLs, respond to security incidents, and receive defensive cybersecurity guidance in Arabic and English.

The project is built as a production-style AI system, not just a simple chatbot. It combines rule-based analysis, machine learning models, Retrieval-Augmented Generation (RAG), LLM reasoning, PostgreSQL conversation memory, and a modern React chat interface.

---

## Live Demo

### Frontend
https://cyber-guard-ai-advisor.vercel.app

### Backend API
https://cyberguard-ai-advisor-production.up.railway.app

### API Documentation
https://cyberguard-ai-advisor-production.up.railway.app/docs

---

# Main Features

- Conversational cybersecurity assistant
- Phishing email analysis
- Suspicious URL risk detection
- Incident response guidance
- Defensive cybersecurity recommendations
- Arabic and English support
- Rule-based security analysis
- ML-based phishing email detection
- ML-based URL risk classification
- Retrieval-Augmented Generation (RAG)
- PostgreSQL conversation memory
- Hugging Face model hosting
- OpenRouter LLM integration
- FastAPI backend
- React + Vite frontend
- Dockerized deployment
- Cloud deployment pipeline

---

# System Architecture

## Frontend Layer
- React + Vite frontend
- Hosted on Vercel
- Modern chat-based cybersecurity UI
- Axios communication with backend APIs

---

## Backend Layer
- FastAPI backend hosted on Railway
- REST API architecture
- Modular service-based structure
- Handles:
  - Chat requests
  - URL analysis
  - Email phishing detection
  - RAG responses
  - Conversation memory

---

## AI & ML Layer

### Rule-Based Analysis
- URL heuristics
- Security keyword detection
- Risk scoring

### Machine Learning Models
- DistilBERT phishing email classifier
- Scikit-learn URL risk classifier
- Models hosted on Hugging Face Hub

### RAG Pipeline
- FAISS vector store
- sentence-transformers embeddings
- Cybersecurity knowledge base
- OpenRouter LLM generation

---

## Database Layer
- PostgreSQL database hosted on Neon
- Stores:
  - Chat sessions
  - Chat messages
  - Security events
  - Conversation history

---

## Deployment Layer
- Frontend deployed on Vercel
- Backend deployed on Railway
- Database hosted on Neon
- ML models hosted on Hugging Face

---

# Tech Stack

## Backend
- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- FAISS
- sentence-transformers
- Transformers
- scikit-learn
- Hugging Face Hub
- OpenRouter API
- Docker

---

## Frontend
- React
- Vite
- Axios
- Lucide React
- CSS

---

## Deployment & Infrastructure
- Railway
- Vercel
- Neon PostgreSQL
- Hugging Face Hub

---

# Project Structure

```text
CyberGuard-AI-Advisor/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── ml/
│   │   ├── db/
│   │   ├── knowledge_base/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

# Chat Processing Pipeline

When a user sends a message:

1. The React frontend sends the request to the FastAPI backend.
2. The backend creates or resumes a chat session.
3. The user message is stored in PostgreSQL.
4. The backend detects the message type:
   - Suspicious URL
   - Phishing email
   - General cybersecurity question
   - Incident response request
5. The correct processing pipeline is selected:
   - Rule-based analysis
   - Machine learning classification
   - RAG retrieval
   - LLM generation
6. The assistant response is generated.
7. The response is stored in PostgreSQL.
8. The final answer is returned to the frontend.

---

# Machine Learning Models

## Email Phishing Detection

The phishing email detector is based on a fine-tuned DistilBERT model.

Hosted on Hugging Face Hub:

```text
rawankhaled46/cyberguard-email-phishing-model
```

The backend dynamically downloads the model during deployment instead of storing large model files in GitHub.

---

## URL Risk Detection

The suspicious URL detector uses a scikit-learn classification model.

Hosted on Hugging Face Hub:

```text
rawankhaled46/cyberguard-url-model
```

The model is downloaded dynamically using `huggingface_hub`.

---

# Retrieval-Augmented Generation (RAG)

CyberGuard uses RAG to answer cybersecurity questions using a curated cybersecurity knowledge base.

## RAG Flow

1. User question
2. Text embedding generation
3. FAISS similarity search
4. Retrieve relevant cybersecurity context
5. OpenRouter LLM response generation
6. Final defensive cybersecurity answer

The knowledge base includes:
- Phishing awareness
- Password safety
- Suspicious URL guidance
- Incident response recommendations
- Defensive cybersecurity best practices

---

# Safety Layer

CyberGuard includes a safety layer to prevent offensive cybersecurity misuse.

The assistant refuses requests related to:
- Malware creation
- Credential theft
- Exploit development
- Hacking instructions
- Phishing kit generation
- Security bypass techniques

Instead, the assistant redirects users toward defensive and ethical cybersecurity practices.

---

# Environment Variables

Create a `.env` file inside the backend directory:

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

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

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

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

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

Run the frontend:

```bash
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

---

# Running with Docker

Build the backend image:

```bash
docker build -t cyberguard-backend .
```

Run the backend container:

```bash
docker run -p 8000:8000 --env-file .env cyberguard-backend
```

---

# Database Migrations

Alembic is used for database schema management.

Create a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Production deployments automatically run migrations before starting the backend service.

---

# Deployment

## Backend
- Hosted on Railway
- Dockerized FastAPI deployment
- Automatic PostgreSQL migrations during startup

Startup command:

```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Frontend
- Hosted on Vercel
- React + Vite deployment

---

## Database
- PostgreSQL hosted on Neon

---

## ML Models
- Hosted on Hugging Face Hub
- Dynamically downloaded during deployment

---

# API Endpoints

## Chat Endpoint

```http
POST /chat/
```

Example request:

```json
{
  "message": "I clicked a suspicious link, what should I do?"
}
```

---

## URL Analysis

```http
POST /url/analyze
```

---

## Email Analysis

```http
POST /email/analyze
```

---

## Password Analysis

```http
POST /password/check
```

---

# Engineering Decisions

## Why PostgreSQL instead of SQLite?
PostgreSQL was selected because the project requires persistent conversation memory, production-style deployment, scalability, and reliable schema migrations.

---

## Why Docker?
Docker ensures consistent backend execution across local development and cloud deployment environments.

---

## Why Railway?
Railway supports Dockerized FastAPI applications and provides simple backend deployment workflows.

---

## Why Vercel?
Vercel is optimized for React frontend hosting and CDN-based delivery.

---

## Why Neon?
Neon provides managed PostgreSQL with SSL support and easy cloud integration.

---

## Why Hugging Face Hub?
Hugging Face Hub acts as a model registry for storing and loading ML models dynamically during deployment.

---

# Current Limitations

- Authentication is not implemented yet
- Rate limiting is planned
- ML models may require additional evaluation
- The system focuses only on defensive cybersecurity
- The assistant should not replace professional incident response teams

---

# Future Improvements

- User authentication
- User-specific memory
- Security report export
- File upload for phishing email analysis
- Better logging and observability
- Admin dashboard
- CI/CD testing pipeline
- Advanced Arabic cybersecurity knowledge base
- Dedicated ML inference service
- Improved model monitoring

---

# Current Status

CyberGuard AI Advisor is currently deployed as a live production-style AI cybersecurity assistant with:

- React frontend
- FastAPI backend
- PostgreSQL memory system
- RAG-based cybersecurity responses
- Hugging Face-hosted ML models
- Cloud deployment pipeline

---

# Author

Developed by Rawan Khaled.

GitHub:
https://github.com/Rawan-khaled-AI