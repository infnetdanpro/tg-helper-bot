# This file include function by name
import os
from random import randint
import markovify
from random import randint
import requests
from conf import config


commands = {}


def command(command): 
    def wrapper(func): 
        commands[command[1:]] = func
        return func
    return wrapper


@command('/cats')
def get_random_cats(search_query: str = 'cats'):
    """Get random cats"""
    resp: dict = {
        'result_type': None, 
        'result': None
    }

    headers = {'Authorization': config.PEXELS_IMAGE_API_TOKEN}
    params = {'query': search_query or 'cats', 'page': randint(1,2852), 'per_page': 1}

    r = requests.get(url=config.PEXELS_IMAGE_API_URL, params=params, headers=headers)
    data: dict = r.json()
    
    if r.status_code == 200 and data:
        resp['result_type'] = 'photo'
        resp['result']: str = data['photos'][-1]['src']['large']
    
    return resp


@command('/echo')
def echo(text: str):
    """Test echo function"""
    return {'result_type': 'text', 'result': text}


@command('/bad_harry')
def bad_harry(*args):
    """Very bad Harry Potter 18+"""
    with open('text\\sodom.txt', encoding='utf-8') as f:
        text_a = f.read()

    with open('text\\potter.txt', encoding='utf-8') as f:
        text_b = f.read()

    model_a = markovify.Text(text_a)
    model_b = markovify.Text(text_b)
    model_combo = markovify.combine([model_a, model_b], [2, 0.1])
    # model_combo.compile(inplace=True)

    # TODO: use other way to create short sentence
    while True:
        res = model_combo.make_short_sentence(max_chars=randint(50, 300), tries=randint(50, 500))

        if not res:
            continue
        if 'гарри' in res.lower() and res.endswith('.'):
            text = res[:1].title() + res[1:]
            return {'result_type': 'text', 'result': text}
