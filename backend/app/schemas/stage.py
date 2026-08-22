from typing import Optional

from pydantic import BaseModel


class StageCreate(BaseModel):
    name: str
    description: Optional[str] = None
    order: Optional[int] = 0
