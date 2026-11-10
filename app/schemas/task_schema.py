from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskCreateSchema(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: Optional[str] = None


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=150
    )
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    completed: bool