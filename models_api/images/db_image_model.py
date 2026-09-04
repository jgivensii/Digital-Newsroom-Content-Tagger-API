from sqlalchemy import ForeignKey, String, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from content_api.extensions import db
from datetime import datetime, timezone
from uuid import UUID, uuid4

class ImageRecord(db.Model):
    __tablename__ = "images"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True,default=uuid4, nullable=False)
    article_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), unique=True)
    featured_image_key: Mapped[str]= mapped_column(String, nullable=False)
    labels: Mapped[list[str]]= mapped_column(ARRAY(String), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc))
    articles: Mapped["ArticleRecord"] = relationship(back_populates="images")

