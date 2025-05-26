"""
RAG (Retrieval-Augmented Generation) service implementation.
"""
from typing import List, Dict, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from core.config import get_settings
from core.exceptions import DocumentProcessingError, QuestionAnsweringError, VectorStoreError
from db.repositories.document import DocumentRepository
from db.repositories.embedding import EmbeddingRepository
from utils.text_processing import clean_text, extract_metadata

settings = get_settings()

class RAGService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        embedding_repository: EmbeddingRepository
    ):
        self.document_repository = document_repository
        self.embedding_repository = embedding_repository
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_API_BASE
        )
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_API_BASE
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_document(self, content: str, metadata: Dict[str, Any]) -> int:
        """Process a document and store its embeddings."""
        try:
            # Clean and preprocess text
            cleaned_content = clean_text(content)
            
            # Extract metadata
            extracted_metadata = extract_metadata(cleaned_content)
            metadata.update(extracted_metadata)
            
            # Split document into chunks
            chunks = self.text_splitter.split_text(cleaned_content)
            
            # Store document
            document_id = self.document_repository.create(
                content=cleaned_content,
                metadata=metadata
            )
            
            # Create and store embeddings for each chunk
            for i, chunk in enumerate(chunks):
                embedding = self.embeddings.embed_query(chunk)
                self.embedding_repository.create(
                    document_id=document_id,
                    content=chunk,
                    embedding=embedding,
                    metadata={"chunk_index": i}
                )
            
            return document_id
        except Exception as e:
            raise DocumentProcessingError(
                "Error processing document",
                details={"error": str(e)}
            )

    def answer_question(
        self,
        question: str,
        document_id: Optional[int] = None,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """Answer a question using RAG."""
        try:
            # Get relevant embeddings
            if document_id:
                embeddings = self.embedding_repository.get_by_document(document_id)
            else:
                embeddings = self.embedding_repository.get_all()
            
            if not embeddings:
                raise QuestionAnsweringError("No relevant documents found")
            
            # Create vector store
            texts = [e.content for e in embeddings]
            vectors = [e.embedding for e in embeddings]
            metadatas = [{"source": str(e.document_id), "chunk_index": e.metadata.get("chunk_index", 0)} for e in embeddings]
            
            vector_store = FAISS.from_embeddings(
                text_embeddings=list(zip(texts, vectors)),
                embedding=self.embeddings,
                metadatas=metadatas
            )
            
            # Create QA chain with custom prompt
            prompt_template = """
            Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            Use three sentences maximum and keep the answer concise.
            
            Context: {context}
            
            Question: {question}
            
            Answer: Let me help you with that.
            """
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(search_kwargs={"k": top_k}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt}
            )
            
            # Get answer
            result = qa_chain({"query": question})
            
            # Calculate confidence score
            confidence = self._calculate_confidence(result)
            
            return {
                "answer": result["result"],
                "confidence": confidence,
                "sources": [
                    {
                        "document_id": doc.metadata["source"],
                        "chunk_index": doc.metadata["chunk_index"]
                    }
                    for doc in result["source_documents"]
                ]
            }
        except Exception as e:
            raise QuestionAnsweringError(
                "Error answering question",
                details={"error": str(e)}
            )

    def generate_summary(self, document_id: int) -> str:
        """Generate a summary of a document."""
        try:
            # Get document
            document = self.document_repository.get(document_id)
            if not document:
                raise DocumentProcessingError(
                    "Document not found",
                    details={"document_id": document_id}
                )
            
            # Split into chunks
            chunks = self.text_splitter.split_text(document.content)
            
            # Summarize each chunk
            summaries = []
            for chunk in chunks:
                prompt = f"""
                Summarize the following text concisely in one sentence:
                
                {chunk}
                """
                response = self.llm.predict(prompt)
                summaries.append(response)
            
            # Combine summaries
            combined_summary = "\n".join(summaries)
            final_prompt = f"""
            Create a concise summary from these points. The summary should be coherent and well-structured:
            
            {combined_summary}
            """
            final_summary = self.llm.predict(final_prompt)
            
            return final_summary
        except Exception as e:
            raise DocumentProcessingError(
                "Error generating summary",
                details={"error": str(e)}
            )

    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for the answer."""
        # This is a simple implementation. In production, you might want to use
        # more sophisticated methods like semantic similarity or model confidence scores.
        source_docs = result.get("source_documents", [])
        if not source_docs:
            return 0.0
        
        # Calculate confidence based on number of relevant sources
        num_sources = len(source_docs)
        max_sources = 3  # Maximum number of sources we expect
        
        return min(num_sources / max_sources, 1.0) 