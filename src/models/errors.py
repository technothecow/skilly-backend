from typing import Optional

from pydantic import BaseModel


class Error(BaseModel):
    message: str
    code: Optional[str] = None
    details: Optional[str] = None
