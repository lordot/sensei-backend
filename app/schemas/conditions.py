from pydantic import BaseModel, Field

from ..models.enums import Level, Type


class ConditionRead(BaseModel):
    id: int
    level: Level
    type: Type | None
    text: str

    class Config:
        orm_mode = True


class ConditionCreate(BaseModel):
    level: Level
    type: Type | None
    text: str = Field(..., max_length=250)


class ConditionUpdate(BaseModel):
    pass
