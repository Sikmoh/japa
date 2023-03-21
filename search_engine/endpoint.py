import os
import openai
from basehandler import api_response
from auth.core import permission
from errors.v1.handlers import ApiError


def search(**kwargs):
    """
            Fetch info about a destination
        :return: answer
        :errors:
            raises an APIError
        """
    permission(kwargs['token_info'], access_role='basic')
    openai.api_key = os.getenv("OPENAI_API_KEY")

    start_sequence = "\nA:"
    restart_sequence = "\n\nQ: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, "
               "I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear "
               "answer, I will respond with \"Unknown\".\n\nQ:{question}\nA:".format(question=kwargs['question']),
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    if response.choices[0].text == '':
        raise ApiError('No answer found', 404)
    else:
        return api_response({'result': response.choices[0].text})
