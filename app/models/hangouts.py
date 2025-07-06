from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class HangoutPostBase(BaseModel):
    """Base model for hangout posts"""
    username: str
    imageUrl: str
    description: str
    tags: List[str] = []

class HangoutPostCreate(HangoutPostBase):
    """Model for creating a hangout post"""
    pass

class HangoutPost(HangoutPostBase):
    """Model for returning a hangout post"""
    id: str = Field(..., alias="_id")
    likes: int = 0
    comments: int = 0
    created_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        populate_by_name = True
