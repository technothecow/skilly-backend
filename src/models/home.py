from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class RecommendedUser(BaseModel):
    display_name: str = Field(..., min_length=1)
    teach_categories: List[str] = Field(..., min_items=1)
    learn_categories: List[str] = Field(..., min_items=1)
    username: str = Field(..., min_length=1)
    photo: str = Field(..., min_length=0)


class Chat(BaseModel):
    id: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    photo: str = Field(..., min_length=0)
    last_message: str = Field(..., min_length=0)
    status: str = Field(..., enum=['sent', 'read', 'unread'])


class Event(BaseModel):
    name: str = Field(..., min_length=1)
    id: str = Field(..., min_length=1)
    datetime: datetime
    description: str = Field(..., min_length=1)


class HomeData(BaseModel):
    username: str = Field(..., min_length=1)
    learn_categories: List[str] = Field(..., min_items=1)
    teach_categories: List[str] = Field(..., min_items=1)
    recommended: List[RecommendedUser]
    chats: List[Chat]
    events: List[Event]
    is_maintained: bool

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
