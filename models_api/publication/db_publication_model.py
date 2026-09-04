from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from content_api.extensions import db
from datetime import datetime, timezone
from uuid import UUID, uuid4


class PublicationRecord(db.Model):
    __tablename__ = "publications"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default= uuid4, nullable=False)
    name: Mapped[str]= mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default = lambda: datetime.now(timezone.utc))
    articles: Mapped[list["ArticleRecord"]] = relationship(back_populates= "publication", cascade="all, delete-orphan")

