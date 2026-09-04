from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from content_api.extensions import db
from models_api.shared import Status, Status_analysis
from datetime import datetime, timezone
from uuid import UUID, uuid4

""
class ArticleRecord(db.Model):
    __tablename__ = "articles"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True,default=uuid4, nullable=False)
    publication_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),ForeignKey("publications.id", ondelete="CASCADE"))
    author: Mapped[str]= mapped_column(String(20), nullable=False)
    title: Mapped[str]= mapped_column(String(20), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc))
    status: Mapped[Status] = mapped_column(nullable=False)
    status_analysis: Mapped[Status_analysis] = mapped_column(nullable=False)
    publication: Mapped["PublicationRecord"] = relationship(back_populates="articles")
    images: Mapped["ImageRecord"] = relationship(back_populates="articles", uselist=False, cascade="all, delete-orphan")
    tag: Mapped["TagExtractionRecord"] = relationship(back_populates="articles")