import openai

from app.core.config import get_settings
from app.models import Condition
from app.models.exercises import Exercise

openai.api_key = get_settings().openai_api_key
openai.organization = get_settings().openai_org

TEMPERATURE = 0.3
MAX_TOKENS = 300
MODEL = "gpt-3.5-turbo-16k"
SYS_CONTENT = (
    "You are a English teacher. Check my answers. Do not repeat user answer."
    "Explain the mistakes and suggest how the sentence can be improved. "
    "At the end, indicate the verdict: Accepted, rejected"
)

INIT_MSG = (
    'Question:\n {exercise}'
    'Conditions:\n {conditions}'
)


async def make_query_message(
        exercise: Exercise,
        conditions: list[Condition | None],
        answer: str
):
    conditions_str = '\n'.join([c.text for c in conditions if c])
    query_message: list = [
        {"role": "system", "content": SYS_CONTENT},
        {"role": "user", "content": INIT_MSG.format(
            exercise=exercise.question,
            conditions=conditions_str
        )},
        {"role": "user", "content": "Check my answer: " + answer},
    ]
    return query_message


async def get_exam_from_openai(
        exercise: Exercise,
        conditions: list[Condition | None],
        answer: str
):
    query_message = await make_query_message(exercise, conditions, answer)
    try:
        response = await openai.ChatCompletion.acreate(
            model=MODEL,
            messages=query_message,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
    except openai.error.OpenAIError as e:
        print(f'Error: {e}')
        return "Sorry, I am a little busy now. Try again later."  # TODO: add variable with this message
    out_t, in_t, _ = response.usage.values()
    exam = response.choices[0].message.content
    print(f'Out tokens: {out_t}, In tokens: {in_t}')
    return exam
