# AI Knowledge Assistant

An AI-powered document question-answering platform built using **React**, **Express**, **FastAPI**, **LangChain**, **Google Gemini**, and **ChromaDB**. The application enables users to upload PDF documents and interact with them through intelligent conversations powered by Retrieval-Augmented Generation (RAG).

The system combines semantic search, keyword search, history-aware retrieval, multi-query retrieval, reranking, and Google's Gemini LLM to generate accurate, context-aware answers grounded in the uploaded documents.

---

## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- React Router

### Backend

- Node.js
- Express.js
- MongoDB
- Mongoose
- JWT Authentication
- Multer

### AI Service

- FastAPI
- LangChain
- Google Gemini API
- ChromaDB
- BM25
- Hybrid Retrieval
- Multi Query Retrieval
- History Aware Retrieval
- Reciprocal Rank Fusion (RRF)
- Cross Encoder Reranker

### Database

- MongoDB
- Chroma Vector Database

### Deployment

- Docker
- Docker Compose
- AWS EC2
- MongoDB Atlas

---

# Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Protected Routes
- Persistent Login

---

## Document Management

- Upload PDF Documents
- View Uploaded Documents
- Delete Documents
- Automatic PDF Processing
- Automatic Embedding Generation

---

## AI Chat

- Multiple Chat Sessions
- Continue Previous Conversations
- Delete Chat Sessions
- History Aware Conversations
- Context-aware Answers
- Multi Query Retrieval
- Hybrid Search
- Document Grounded Responses

---

## Retrieval Pipeline

- Recursive Character Chunking
- Gemini Embeddings
- Chroma Vector Search
- BM25 Keyword Search
- Hybrid Retrieval
- History Aware Retrieval
- Multi Query Retrieval
- Reciprocal Rank Fusion (RRF)
- Cross Encoder Reranking
- Google Gemini Response Generation

---

# Architecture

```text
                     React Frontend
                           │
                           ▼
                    Express Backend
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
      MongoDB Atlas                FastAPI AI Service
                                            │
                                            ▼
                                   Retrieval Pipeline
                                            │
      ┌─────────────┬──────────────┬──────────────┐
      ▼             ▼              ▼              ▼
 Chunking     Embeddings       ChromaDB        BM25
                                            │
                                            ▼
                                 History Aware Retrieval
                                            │
                                            ▼
                                 Multi Query Retrieval
                                            │
                                            ▼
                                     Hybrid Retrieval
                                            │
                                            ▼
                              Reciprocal Rank Fusion
                                            │
                                            ▼
                              Cross Encoder Reranker
                                            │
                                            ▼
                                   Google Gemini
```

---

# Retrieval Pipeline

```text
PDF Upload
      │
      ▼
Text Extraction
      │
      ▼
Recursive Chunking
      │
      ▼
Gemini Embeddings
      │
      ▼
ChromaDB
      │
      ▼
History Aware Retrieval
      │
      ▼
Multi Query Generation
      │
      ▼
Vector Retrieval
      │
      ├──────────────┐
      ▼              ▼
Vector Search      BM25 Search
      │              │
      └──────┬───────┘
             ▼
      Hybrid Retrieval
             │
             ▼             
Reciprocal Rank Fusion
             │
             ▼
Cross Encoder Reranker
             │
             ▼
Google Gemini
             │
             ▼
Final Answer
```

---

# Chat Flow

```text
User Question
      │
      ▼
Express Backend
      │
      ▼
FastAPI AI Service
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
History Aware Retrieval
      │
      ▼
Multi Query Retrieval
      │
      ▼
Reranking
      │
      ▼
Gemini LLM
      │
      ▼
Store Chat History
      │
      ▼
Return Response
```

---

# Project Structure

```text
AI-Knowledge-Assistant/

├── Frontend/
│
├── Backend/
│
├── AI-Service/
│
├── docker-compose.yml
│
└── README.md
```

---

# REST API

## Authentication

| Method | Endpoint |
|----------|-------------------------|
| POST | /api/auth/register |
| POST | /api/auth/login |

---

## Documents

| Method | Endpoint |
|----------|-----------------------------|
| POST | /api/documents/upload |
| GET | /api/documents |
| DELETE | /api/documents/:id |

---

## Chat

| Method | Endpoint |
|----------|------------------------------|
| GET | /api/chat |
| GET | /api/chat/:sessionId |
| POST | /api/chat |
| DELETE | /api/chat/:sessionId |

---

# Environment Variables

## Backend

```env
PORT=

MONGODB_URI=

JWT_SECRET=

AI_SERVICE_URL=
```

---

## AI Service

```env
GOOGLE_API_KEY=

CHROMA_DB_PATH=

CHUNK_SIZE=

CHUNK_OVERLAP=
```

---

## Frontend

```env
VITE_API_URL=
```

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/your-username/AI-Knowledge-Assistant.git

cd AI-Knowledge-Assistant
```

---

## Backend

```bash
cd Backend

npm install

npm run dev
```

---

## AI Service

```bash
cd AI-Service

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd Frontend

npm install

npm run dev
```

---

# Screenshots

## Login Page

<img width="735" height="429" alt="image" src="https://github.com/user-attachments/assets/7773fff8-730d-4101-8b1c-ed796b5d9917" />

---

## Register Page

<img width="747" height="428" alt="image" src="https://github.com/user-attachments/assets/f15269fa-88d2-4101-9d41-cfacc272e9e2" />

---

## Dashboard

<img width="903" height="422" alt="image" src="https://github.com/user-attachments/assets/9416f1f4-0652-4941-9994-2635d9e3c9db" />

---

## Documents Page

<img width="943" height="470" alt="image" src="https://github.com/user-attachments/assets/dbd65328-29f8-4905-960d-983292e1f8ca" />

---

## Chat Interface

<img width="949" height="470" alt="image" src="https://github.com/user-attachments/assets/daa3dedb-2f03-42e3-8ad0-3bd89b70a485" />

---

# Deployment

The project is containerized using Docker and is designed for deployment on AWS.

## Production Architecture

```text
                    AWS EC2
                        │
                Docker Compose
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 React (Nginx)    Express Backend   FastAPI AI
                                          │
                                          ▼
                                   Google Gemini
                                          │
                                          ▼
                                  ChromaDB Volume
                                          │
                                          ▼
                                   MongoDB Atlas
```

Deployment Stack

- Docker
- Docker Compose
- AWS EC2
- MongoDB Atlas
- Google Gemini API

---

# Author

**Devendar Reddy**

B.Tech CSE, IIIT Guwahati

GitHub: https://github.com/Awesomedude666

LinkedIn: https://linkedin.com/in/d4devendar

---

If you found this project useful, consider giving it a ⭐ on GitHub.
