import os
import random

import openai
from dotenv import load_dotenv
from openai.openai_object import OpenAIObject

from grammars import *

load_dotenv('.env')


SYS_CONTENT = (
    "You are a English teacher. Check my answers. "
    "Explain the mistakes and suggest how the sentence can be improved. "
    "Suggest your own answer considering all the conditions of the question."
)
INIT_MSG = (
    'Question:\n'
    f'{random.choice(english_questions_pre_intermediate)}' +
    ' ' + f'{random.choice(grammar_conditions_pre_intermediate)}' +
    ' in at least one of your sentences.'
)
MODEL = "gpt-3.5-turbo-16k"
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORG')

dialog: list = [
    {"role": "system", "content": SYS_CONTENT},
]


def create_chat_completion(request):
    response: OpenAIObject = openai.ChatCompletion.create(
        model=MODEL,
        messages=request,
        temperature=1,
        max_tokens=300
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    dialog.append({"role": "user", "content": INIT_MSG},)
    print(dialog[-1]['content'])
    dialog.append({"role": "user", "content": "Check my answer: " + input()},)
    print(create_chat_completion(dialog))
