from pydantic import BaseModel


class UserAuthentication(BaseModel):
    email: str
    password: str
