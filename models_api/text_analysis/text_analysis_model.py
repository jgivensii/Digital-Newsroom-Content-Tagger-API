from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional


class TagExtraction(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    article_id: Optional[UUID]
    body: str = Field(min_length = 1, max_length=5000)
    tags: list[dict]
    entities: list[dict]

class CreateTagDTO(BaseModel):
    
    model_config = ConfigDict(extra='forbid')
    
    body: str = Field(min_length=1, max_length=5000)
    tags: list[dict]
    entities: list[dict]
    
class UpdateTagDTO(BaseModel):
    
    model_config = ConfigDict(extra='forbid')
    
    body: str = Field(min_length=1, max_length=5000)
    tags: list[dict]
    entities: list[dict]
    
class TrendingEntityDTO(BaseModel):
    
    model_config = ConfigDict(extra='forbid')
    
    publication_id: UUID
    entity: str
    occurrences: int