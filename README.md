### 📄 Fullstack RAG-Based Document Q\&A System – Project Documentation


#### 🧠 Project Overview

This is a fullstack document management and Q\&A system powered by Retrieval-Augmented Generation (RAG). The system allows users to upload `.pdf` or `.txt` files, converts them into vector embeddings using OpenAI, stores them in FAISS, and allows users to ask questions and receive LLM-generated answers.


#### 🔧 Tech Stack

* **Backend**: FastAPI (Python), SQLAlchemy
* **Embeddings + RAG**: OpenAI + LangChain + FAISS
* **Frontend**: React (with Axios and React Router)
* **Database**: PostgreSQL
* **Authentication**: JWT-based (Login + Protected Routes)
* **Containerization**: Docker, Docker Compose


#### 🗂 Folder Structure

fullstack-rag-app/
│
├── backend/                # FastAPI backend
│   ├── routers/            # API routers: auth, documents, qa
│   ├── services/           # Document ingestion and QA engine
│   ├── db/                 # Models and DB init
│   ├── core/               # Pydantic settings config
│   └── main.py             # Entry point
│
├── frontend/               # React frontend
│   ├── pages/              # Login, Dashboard, QA
│   ├── components/         # Navbar, Uploader
│   └── App.js / index.js
│
├── docker-compose.yml      # Docker multi-service orchestration
├── .env                    # Environment variables
└── README.md

#### ⚙️ Environment Variables (.env)

Create a `.env` file in the root with:


DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/ragdb
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx


#### 🐳 How to Run the App with Docker

Step-by-step setup:

1. Clone the project:

   ```
   git clone https://github.com/your-org/fullstack-rag-app.git
   cd fullstack-rag-app
   ```

2. Run the application:

   ```
   docker-compose up --build
   ```

3. Visit the following:

   * Frontend UI: [http://localhost:3000](http://localhost:3000)
   * FastAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)


#### 🧩 Key Features

* JWT-based login and authentication
* Secure document upload (.pdf and .txt)
* Embedding generation using OpenAI
* FAISS vector index for semantic search
* Question answering via LangChain + LLM
* React-based UI with login, upload, and Q\&A panels


#### 🔐 Authentication Workflow

1. User logs in via `/auth/login`
2. Backend issues a JWT token
3. Token is stored in browser `localStorage`
4. Protected routes (upload, QA) validate token via middleware


#### 📤 Document Ingestion Flow

1. User uploads a `.pdf` or `.txt` file
2. File is saved and parsed
3. Embeddings are generated using `OpenAIEmbeddings`
4. Embeddings stored in `FAISS` index locally
5. Metadata is saved in PostgreSQL


#### ❓ Question Answering Flow (RAG)

1. User types a question
2. Backend loads FAISS index and retrieves top-k documents
3. LLM (OpenAI) is invoked via `load_qa_chain`
4. Answer is returned based on retrieved context


#### 🔍 Testing and Debugging

To run backend unit tests:

bash
cd backend
pytest tests/


To debug FAISS or OpenAI failures, logs are printed inside:

services/qa_engine.py
services/doc_ingestor.py

#### 🐘 PostgreSQL Setup (Docker)

* Username: `postgres`
* Password: `postgres`
* DB Name: `ragdb`
* Port: `5432`

Docker volume persists data using `postgres_data`.

#### 📁 Docker Compose (3 Services)

* `backend`: FastAPI with volume-mount and .env support
* `frontend`: React served via `npm start`
* `db`: Postgres 15 with initialized volume


#### 🔄 API Summary

| Endpoint            | Method | Description                    |
| ------------------- | ------ | ------------------------------ |
| `/auth/login`       | POST   | Login with username/password   |
| `/documents/upload` | POST   | Upload document (JWT required) |
| `/qa/`              | POST   | Ask question (JWT required)    |
| `/auth/test-token`  | GET    | Test JWT token validity        |

# Fullstack RAG Application

A fullstack application that implements Retrieval-Augmented Generation (RAG) for document processing and question answering.

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- LangChain
- OpenAI
- FAISS
- Alembic
- Pytest

### Frontend
- React
- TypeScript
- Vite
- React Router
- Axios
- TailwindCSS

## Features

- Document processing and embedding generation
- Vector similarity search
- Question answering with context
- Document summarization
- User authentication
- Secure API endpoints
- Modern UI/UX

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- OpenAI API key

## Environment Variables

Create `.env` files in both `backend` and `frontend` directories:

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/rag_db
OPENAI_API_KEY=your_openai_api_key
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-3.5-turbo
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=RAG Application
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fullstack-rag-app.git
cd fullstack-rag-app
```

2. Start the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

3. Start the frontend:
```bash
cd frontend
npm install
npm run dev
```

4. Run tests:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Docker Setup

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec backend alembic upgrade head
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
fullstack-rag-app/
├── backend/
│   ├── alembic/
│   ├── api/
│   │   └── v1/
│   ├── core/
│   ├── db/
│   │   ├── models/
│   │   └── repositories/
│   ├── services/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   └── tests/
└── docker-compose.yml
```

## Development

### Backend Development
- Follow PEP 8 style guide
- Write tests for new features
- Update API documentation
- Use type hints
- Handle errors properly

### Frontend Development
- Follow TypeScript best practices
- Write component tests
- Use proper state management
- Follow React best practices
- Implement proper error handling

## Deployment

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Set up production environment variables

3. Deploy using Docker:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT