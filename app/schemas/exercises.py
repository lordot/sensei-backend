from pydantic import BaseModel

from ..models.exercises import Level


class ExWritingRead(BaseModel):
    id: str
    level: Level
    question: str

    class Config:
        orm_mode = True


class ExWritingCreate(BaseModel):
    level: Level
    question: str
