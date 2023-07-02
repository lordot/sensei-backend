from app.models import Condition
from app.models.exercises import Exercise

SYS_CONTENT = (
    "You are a English teacher. Check my answers. "
    "Explain the mistakes and suggest how the sentence can be improved. "
    "Suggest your own answer considering all the conditions of the question."
)

INIT_MSG = (
    'Question:\n {exercise}'
)


async def get_examination_from_openai(
        exercise: Exercise,
        conditions: list[Condition | None],
        answer: str
):
    pass
