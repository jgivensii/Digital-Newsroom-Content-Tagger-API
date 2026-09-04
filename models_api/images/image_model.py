from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models_api.shared import Status, Status_analysis
from uuid import UUID
from datetime import datetime

class Images(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    article_id: Optional[UUID]
    featured_image_key: str
    labels: list[str]
    created_at: datetime
    updated_at: datetime
