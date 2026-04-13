from datetime import datetime

from pydantic import BaseModel


class BlogCreate(BaseModel):
    title: str
    content: str
    author: str


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime

    model_config = {"from_attributes": True}
