"""
Schema definitions for document data and uploads.
"""

from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    title: str
    uploaded_at: datetime

    class Config:
        orm_mode = True
