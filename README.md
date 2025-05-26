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

A modern fullstack application that implements a RAG (Retrieval-Augmented Generation) system for document processing and question answering.

## Features

- Document processing and embedding generation
- Question answering using RAG
- User authentication and authorization
- API documentation with Swagger/OpenAPI
- Comprehensive test suite
- Database migrations with Alembic
- Logging and error handling

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- Docker and Docker Compose (for containerized deployment)

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fullstack-rag-app.git
cd fullstack-rag-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
python backend/scripts/run_migrations.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start development server:
```bash
npm start
```

## Development

### Backend Development

1. Start the development server:
```bash
uvicorn backend.main:app --reload
```

2. Run tests:
```bash
pytest
```

3. Generate new database migrations:
```bash
alembic revision --autogenerate -m "description of changes"
```

### Frontend Development

1. Start the development server:
```bash
cd frontend
npm start
```

2. Run tests:
```bash
npm test
```

3. Build for production:
```bash
npm run build
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Run migrations in the container:
```bash
docker-compose exec backend python scripts/run_migrations.py
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── api/                  # API routes and endpoints
├── core/                 # Core functionality
├── db/                   # Database models and session
├── services/            # Business logic services
├── tests/               # Test suite
└── scripts/             # Utility scripts

frontend/
├── src/                 # Source code
├── public/             # Static files
├── tests/              # Test files
└── package.json        # Dependencies and scripts
```

## Vector Store

The application uses FAISS for vector storage:
- Embeddings are generated using OpenAI's embedding model
- Vectors are stored in FAISS index
- Index is persisted to disk and loaded on startup
- Vector similarity search is used for document retrieval

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.