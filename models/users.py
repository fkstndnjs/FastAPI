from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
