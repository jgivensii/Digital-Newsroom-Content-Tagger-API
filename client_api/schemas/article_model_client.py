from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class ArticleClient(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    publication_id: Optional[UUID] = None
    title: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1)
    author: Optional[str] = Field(default=None, min_length=1, max_length=200)
    created_at: datetime
    updated_at: datetime
