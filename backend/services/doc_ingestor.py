"""
Handles document ingestion and embedding generation.
"""
import os
import shutil
import traceback
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from db.models import Document
from db.init_db import AsyncSessionLocal
from core.settings import settings

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_and_ingest_file(file, user_id: int) -> bool:
    try:
        # Save file to disk
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Determine loader based on file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        # Load and embed
        documents = loader.load()
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        vector_store = FAISS.from_documents(documents, embeddings)
        vector_store.save_local("faiss_index")

        # Save metadata to DB
        async with AsyncSessionLocal() as session:
            doc = Document(title=file.filename,
                           file_path=file_path, owner_id=user_id)
            session.add(doc)
            await session.commit()

        return True

    except Exception as e:
        print(f"Error during ingestion: {e}")
        traceback.print_exc()
        return False
