from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class PublicationClient(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: str = Field(min_length = 5)
    created_at: datetime