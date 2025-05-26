from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship
from db.base_class import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    embedding = Column(ARRAY(Float), nullable=False)
    content = Column(String, nullable=False)

    # Relationships
    document = relationship("Document", back_populates="embeddings") 