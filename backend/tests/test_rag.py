import pytest
from unittest.mock import Mock, patch
from services.rag import RAGService
from models.document import Document
from db.repositories.base import BaseRepository

@pytest.fixture
def rag_service(test_db):
    document_repository = BaseRepository(Document)
    return RAGService(document_repository)

@pytest.mark.asyncio
async def test_process_document(rag_service, test_db):
    # Mock the FAISS vector store
    with patch('services.rag.FAISS') as mock_faiss:
        mock_faiss.from_texts.return_value = Mock()
        mock_faiss.from_texts.return_value.save_local = Mock()
        
        # Test document processing
        content = "This is a test document content."
        metadata = {"filename": "test.txt"}
        
        document = await rag_service.process_document(content, metadata)
        
        assert document is not None
        assert document.content == content
        assert document.metadata == metadata
        assert document.vector_store_path == f"faiss_index/{metadata['filename']}"
        
        # Verify FAISS was called correctly
        mock_faiss.from_texts.assert_called_once()
        mock_faiss.from_texts.return_value.save_local.assert_called_once()

@pytest.mark.asyncio
async def test_answer_question(rag_service, test_db):
    # Mock the document repository and FAISS
    with patch('services.rag.FAISS') as mock_faiss, \
         patch.object(rag_service.document_repository, 'get') as mock_get:
        
        # Setup mocks
        mock_document = Mock()
        mock_document.vector_store_path = "test_path"
        mock_get.return_value = mock_document
        
        mock_vectorstore = Mock()
        mock_faiss.load_local.return_value = mock_vectorstore
        mock_vectorstore.as_retriever.return_value = Mock()
        
        # Mock the QA chain
        with patch('services.rag.RetrievalQA') as mock_qa:
            mock_qa.from_chain_type.return_value = Mock()
            mock_qa.from_chain_type.return_value.return_value = {"result": "Test answer"}
            
            # Test question answering
            answer = await rag_service.answer_question("Test question?", 1)
            
            assert answer == "Test answer"
            mock_get.assert_called_once_with(1)
            mock_faiss.load_local.assert_called_once_with(
                mock_document.vector_store_path,
                rag_service.embeddings
            )

@pytest.mark.asyncio
async def test_get_document_summary(rag_service, test_db):
    # Mock the document repository and LLM
    with patch.object(rag_service.document_repository, 'get') as mock_get, \
         patch.object(rag_service.llm, 'agenerate') as mock_llm:
        
        # Setup mocks
        mock_document = Mock()
        mock_document.content = "Test content"
        mock_get.return_value = mock_document
        
        mock_llm.return_value.generations = [[Mock(text="Test summary")]]
        
        # Test summary generation
        summary = await rag_service.get_document_summary(1)
        
        assert summary == "Test summary"
        mock_get.assert_called_once_with(1)
        mock_llm.assert_called_once()

@pytest.mark.asyncio
async def test_answer_question_document_not_found(rag_service, test_db):
    # Mock the document repository to return None
    with patch.object(rag_service.document_repository, 'get') as mock_get:
        mock_get.return_value = None
        
        # Test question answering with non-existent document
        with pytest.raises(ValueError, match="Document not found"):
            await rag_service.answer_question("Test question?", 999) 