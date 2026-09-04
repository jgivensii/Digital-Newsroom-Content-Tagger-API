from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from content_api.extensions import db
from uuid import UUID, uuid4

class TagExtractionRecord(db.Model):
    __tablename__ = "tagextraction"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4, nullable=False)
    article_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
    entities: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
    articles: Mapped["ArticleRecord"] = relationship(back_populates="tag")   
    
