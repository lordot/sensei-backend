from pydantic import BaseModel, Field


class Answer(BaseModel):
    text: str = Field(
        ...,
        title='Answer text',
        min_length=30,
        max_length=300
    )  # TODO: create global variable for min and max
    ex_type: str = Field(..., title='Exercise type')
    exercise_id: int = Field(..., title='Exercise id')
    conditions_id: list[int | None] = Field(..., title='Conditions id')
