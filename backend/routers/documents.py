"""
Router to handle document uploads and management.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Request, status
from services.doc_ingestor import save_and_ingest_file

router = APIRouter()


@router.post("/upload")
async def upload_document(request: Request, file: UploadFile = File(...)):
    """
    Upload a document, generate embeddings, and store metadata for the authenticated user.

    - Requires: Bearer token in Authorization header
    - File types supported: .pdf, .txt
    """
    # Safely get user from request.state
    user = getattr(request.state, "user", None)

    # If user is not present (e.g., missing/invalid token), return 401
    if not user or "id" not in user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Missing or invalid token"
        )

    # Call document ingestion service
    success = await save_and_ingest_file(file, user["id"])

    # If ingestion failed
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Upload failed during ingestion"
        )

    return {"message": "Document uploaded and indexed successfully"}
