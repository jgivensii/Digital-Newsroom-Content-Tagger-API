from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models_api.shared import Status, Status_analysis
from uuid import UUID
from datetime import datetime

class Article(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    publication_id: Optional[UUID]
    title: str = Field(min_length=5, max_length=20)
    body: str = Field(min_length=5)
    author: Optional[str] = Field(min_length=5, max_length=20)
    status: Status
    status_analysis: Status_analysis
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str] = None

class CreateArticleDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str = Field(min_length=5, max_length=20)
    publication_id: UUID
    body: str = Field(min_length=1, max_length=5000)
    author: Optional[str] = Field(min_length=5, max_length=20)

class UpdateArticleDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
        
    title: str = Field(min_length=5, max_length=20)
    body: str = Field(min_length=1, max_length=5000)
    author: Optional[str] = Field(min_length=5, max_length=20)