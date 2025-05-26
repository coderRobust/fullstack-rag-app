from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from core.config import get_settings
from core.exceptions import DocumentNotFoundError, RAGProcessingError
from db.repositories.base import BaseRepository
from models.document import Document
from schemas.document import DocumentCreate, DocumentResponse

settings = get_settings()

class RAGService:
    def __init__(self, document_repository: BaseRepository[Document]):
        self.document_repository = document_repository
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-3.5-turbo"
        )

    async def process_document(self, content: str, metadata: dict) -> Document:
        try:
            # Split text into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Create embeddings and store in vector database
            vectorstore = FAISS.from_texts(chunks, self.embeddings)
            
            # Save document metadata and vector store
            document_data = {
                "content": content,
                "metadata": metadata,
                "vector_store_path": f"faiss_index/{metadata['filename']}"
            }
            document = await self.document_repository.create(document_data)
            
            # Save vector store
            vectorstore.save_local(document.vector_store_path)
            
            return document
        except Exception as e:
            raise RAGProcessingError(f"Error processing document: {str(e)}")

    async def answer_question(self, question: str, document_id: int) -> str:
        try:
            # Get document
            document = await self.document_repository.get(document_id)
            if not document:
                raise DocumentNotFoundError(document_id)
            
            # Load vector store
            vectorstore = FAISS.load_local(
                document.vector_store_path,
                self.embeddings
            )
            
            # Create QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever()
            )
            
            # Get answer
            result = qa_chain({"query": question})
            return result["result"]
        except DocumentNotFoundError:
            raise
        except Exception as e:
            raise RAGProcessingError(f"Error answering question: {str(e)}")

    async def get_document_summary(self, document_id: int) -> str:
        try:
            # Get document
            document = await self.document_repository.get(document_id)
            if not document:
                raise DocumentNotFoundError(document_id)
            
            # Generate summary using LLM
            prompt = f"Please provide a concise summary of the following text:\n\n{document.content}"
            response = await self.llm.agenerate([prompt])
            return response.generations[0][0].text
        except DocumentNotFoundError:
            raise
        except Exception as e:
            raise RAGProcessingError(f"Error generating summary: {str(e)}") 