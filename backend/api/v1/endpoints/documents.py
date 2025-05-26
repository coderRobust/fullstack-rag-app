"""
Document API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from core.exceptions import DocumentProcessingError
from db.session import get_db
from schemas.document import DocumentCreate, DocumentResponse, DocumentList
from services.document import DocumentService
from services.rag import RAGService
from api.deps import get_current_user

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Upload and process a document."""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        
        # Create document service
        document_service = DocumentService()
        
        # Process document
        document = await document_service.process_file(
            db=db,
            file=file,
            content=content,
            user_id=current_user.id
        )
        
        return document
    except DocumentProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get document by ID."""
    try:
        document_service = DocumentService()
        document = await document_service.get_document(
            db=db,
            document_id=document_id,
            user_id=current_user.id
        )
        return document
    except DocumentProcessingError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=DocumentList)
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List user's documents."""
    try:
        document_service = DocumentService()
        documents = await document_service.list_documents(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a document."""
    try:
        document_service = DocumentService()
        await document_service.delete_document(
            db=db,
            document_id=document_id,
            user_id=current_user.id
        )
        return {"message": "Document deleted successfully"}
    except DocumentProcessingError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{document_id}/summarize")
async def summarize_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generate a summary for a document."""
    try:
        rag_service = RAGService()
        summary = await rag_service.generate_summary(
            db=db,
            document_id=document_id,
            user_id=current_user.id
        )
        return {"summary": summary}
    except DocumentProcessingError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") 