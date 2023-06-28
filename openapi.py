import os
import random

import openai
from dotenv import load_dotenv
from openai.openai_object import OpenAIObject

from grammars import *

load_dotenv('.env')


SYS_CONTENT = (
    "You are a English teacher. Point out grammatical errors. Here is "
    "an example: "
    "User response:"
    "I walked, and stop"

    "Your answer:"
    '1. Replace "stop" with "stopped" in the past tense'
    '2. After the word "walked" is not needed exactly'

    "Write the correct answer at the end:\n"
    "I walked and stopped"
)
INIT_MSG = (
    'Question:\n'
    f'{random.choice(english_questions_beginner)}' + ' ' + f'{random.choice(grammar_conditions_beginner)}'
)
MODEL = "gpt-3.5-turbo"
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORG')

request: list = [
    {"role": "system", "content": SYS_CONTENT},
    {"role": "user", "content": 'What is your favorite color and why? Use simple present tense'},
    {"role": "user", "content": 'Check my answer: I like blue because the sky.'}
]


def create_chat_completion():
    response: OpenAIObject = openai.ChatCompletion.create(
        model=MODEL,
        messages=request,
        temperature=1,
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    print(request)
    print(create_chat_completion())
