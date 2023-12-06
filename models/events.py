from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column

# Definition of Event Table Model
class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Primary Key Declaration
    title: str
    image: str
    description: str
    location: str
    tags: List[str] = Field(sa_column=Column(JSON))  # Uses JSON Column Type

    class Config:
        arbitrary_types_allowed = True  # Allows Non-pydantic Field Types

# Definition of Update Request Message Body
class EventUpdate(SQLModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    location: Optional[str]
    tags: Optional[List[str]]
