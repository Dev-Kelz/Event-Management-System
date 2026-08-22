from typing import Optional

from pydantic import BaseModel


class NotificationCreate(BaseModel):
    user_id: int
    event_id: Optional[int] = None
    title: str
    message: str
    type: str
    data: Optional[str] = None
