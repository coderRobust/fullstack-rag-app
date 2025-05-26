"""
Tests for RAG service.
"""
import pytest
from unittest.mock import Mock, patch
from services.rag import RAGService
from core.exceptions import DocumentProcessingError, QuestionAnsweringError
from db.repositories.document import DocumentRepository
from db.repositories.embedding import EmbeddingRepository

@pytest.fixture
def mock_document_repository():
    return Mock(spec=DocumentRepository)

@pytest.fixture
def mock_embedding_repository():
    return Mock(spec=EmbeddingRepository)

@pytest.fixture
def rag_service(mock_document_repository, mock_embedding_repository):
    return RAGService(
        document_repository=mock_document_repository,
        embedding_repository=mock_embedding_repository
    )

def test_process_document_success(rag_service, mock_document_repository, mock_embedding_repository):
    """Test successful document processing."""
    # Arrange
    content = "Test document content"
    metadata = {"title": "Test Document"}
    document_id = 1
    
    mock_document_repository.create.return_value = Mock(id=document_id)
    mock_embedding_repository.create.return_value = Mock(id=1)
    
    # Act
    result = rag_service.process_document(content, metadata)
    
    # Assert
    assert result == document_id
    mock_document_repository.create.assert_called_once()
    assert mock_embedding_repository.create.call_count > 0

def test_process_document_error(rag_service, mock_document_repository):
    """Test document processing error."""
    # Arrange
    content = "Test document content"
    metadata = {"title": "Test Document"}
    
    mock_document_repository.create.side_effect = Exception("Database error")
    
    # Act & Assert
    with pytest.raises(DocumentProcessingError):
        rag_service.process_document(content, metadata)

def test_answer_question_success(rag_service, mock_embedding_repository):
    """Test successful question answering."""
    # Arrange
    question = "What is the test question?"
    mock_embedding = Mock(
        content="Test content",
        embedding=[0.1, 0.2, 0.3],
        document_id=1,
        metadata={"chunk_index": 0}
    )
    mock_embedding_repository.get_all.return_value = [mock_embedding]
    
    # Act
    with patch("services.rag.ChatOpenAI") as mock_llm:
        mock_llm.return_value.predict.return_value = "Test answer"
        result = rag_service.answer_question(question)
    
    # Assert
    assert "answer" in result
    assert "confidence" in result
    assert "sources" in result
    assert isinstance(result["sources"], list)

def test_answer_question_no_documents(rag_service, mock_embedding_repository):
    """Test question answering with no documents."""
    # Arrange
    question = "What is the test question?"
    mock_embedding_repository.get_all.return_value = []
    
    # Act & Assert
    with pytest.raises(QuestionAnsweringError):
        rag_service.answer_question(question)

def test_generate_summary_success(rag_service, mock_document_repository):
    """Test successful summary generation."""
    # Arrange
    document_id = 1
    mock_document = Mock(
        id=document_id,
        content="Test document content"
    )
    mock_document_repository.get.return_value = mock_document
    
    # Act
    with patch("services.rag.ChatOpenAI") as mock_llm:
        mock_llm.return_value.predict.return_value = "Test summary"
        summary = rag_service.generate_summary(document_id)
    
    # Assert
    assert isinstance(summary, str)
    assert len(summary) > 0

def test_generate_summary_document_not_found(rag_service, mock_document_repository):
    """Test summary generation for non-existent document."""
    # Arrange
    document_id = 1
    mock_document_repository.get.return_value = None
    
    # Act & Assert
    with pytest.raises(DocumentProcessingError):
        rag_service.generate_summary(document_id)

def test_calculate_confidence(rag_service):
    """Test confidence score calculation."""
    # Arrange
    result = {
        "source_documents": [
            Mock(metadata={"source": "1", "chunk_index": 0}),
            Mock(metadata={"source": "1", "chunk_index": 1})
        ]
    }
    
    # Act
    confidence = rag_service._calculate_confidence(result)
    
    # Assert
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 1 