from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.embedding import Embedding
from db.repositories.base import BaseRepository

class EmbeddingRepository(BaseRepository[Embedding]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Embedding)

    async def create(
        self,
        document_id: int,
        embedding: List[float],
        content: str
    ) -> Embedding:
        """Create a new embedding."""
        embedding_obj = Embedding(
            document_id=document_id,
            embedding=embedding,
            content=content
        )
        self.session.add(embedding_obj)
        await self.session.commit()
        await self.session.refresh(embedding_obj)
        return embedding_obj

    async def get_by_document(self, document_id: int) -> List[Embedding]:
        """Get all embeddings for a document."""
        query = select(Embedding).where(Embedding.document_id == document_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all(self) -> List[Embedding]:
        """Get all embeddings."""
        query = select(Embedding)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_by_document(self, document_id: int) -> None:
        """Delete all embeddings for a document."""
        query = select(Embedding).where(Embedding.document_id == document_id)
        result = await self.session.execute(query)
        embeddings = result.scalars().all()
        for embedding in embeddings:
            await self.session.delete(embedding)
        await self.session.commit() 