🚀 Deployment Guide for RAG-Based Document Q&A System (FastAPI + React + Docker)
This application is containerized using Docker Compose to orchestrate the following services:

🧠 FastAPI backend with LangChain, FAISS, OpenAI

📦 React frontend for login, upload, Q&A

🛢 PostgreSQL for user and document metadata

✅ Prerequisites
Docker & Docker Compose installed

OpenAI API key available

📁 .env Configuration
Create a .env file in the root directory with the following values:

ini
Copy
Edit
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/ragdb
JWT_SECRET_KEY=supersecretkey
OPENAI_API_KEY=sk-<your-openai-key>
🔧 Steps to Deploy Using Docker
Clone or unzip the project:

bash
Copy
Edit
git clone https://github.com/your-org/fullstack-rag-app.git
cd fullstack-rag-app
Build and run all services using Docker Compose:

bash
Copy
Edit
docker-compose -f docker/docker-compose.yml up --build
Wait 30–60 seconds for services to become available.

🌐 Access URLs
React App: http://localhost:3000

FastAPI Docs: http://localhost:8000/docs

PostgreSQL DB: localhost:5432 (user: user, password: password, db: ragdb)

🧪 Running Tests
To run backend tests:

bash
Copy
Edit
docker exec -it <backend_container_name> pytest
Or locally:

bash
Copy
Edit
cd backend
pytest