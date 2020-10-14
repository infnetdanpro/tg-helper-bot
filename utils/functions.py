# This file include function by name
import os
import markovify
import requests
import itertools

from random import randint
from conf import config
from models.response import BaseResponse, ResultTypes


commands = {}

def command(comand_name): 
    def wrap(f): 
        commands[comand_name[1:]] = f
        return f
    return wrap


@command('/cats')
def command_random_cats(search_query: str = 'cats') -> dict:
    """Get random cats"""
    resp = BaseResponse()

    headers = {'Authorization': config.PEXELS_IMAGE_API_TOKEN}
    params = {'query': search_query or 'cats', 'page': randint(1,2852), 'per_page': 1}

    r = requests.get(url=config.PEXELS_IMAGE_API_URL, params=params, headers=headers)
    data: dict = r.json()
    
    if r.status_code == 200 and data:
        resp.result_type = ResultTypes.photo.value
        resp.result = data['photos'][-1]['src']['large']
    
    return resp.dict()


@command('/echo')
def command_echo(text: str) -> dict:
    """Test echo function"""
    resp = BaseResponse()
    resp.result = text

    return resp.dict()


@command('/bad_harry')
def command_bad_harry(*args) -> dict:
    """Very bad Harry Potter 18+"""
    resp = BaseResponse()

    with open('text\\sodom.txt', encoding='utf-8') as f:
        text_a = f.read()

    with open('text\\potter.txt', encoding='utf-8') as f:
        text_b = f.read()

    model_a = markovify.Text(text_a)
    model_b = markovify.Text(text_b)
    model_combo = markovify.combine([model_a, model_b], [2, 0.1])
    # model_combo.compile(inplace=True)

    # TODO: use other way to create short sentence
    for i in itertools.count(1):
        res = model_combo.make_short_sentence(max_chars=randint(50, 300), tries=randint(50, 500))

        if not res:
            continue
        if 'гарри' in res.lower() and res.endswith('.'):
            text = res[:1].title() + res[1:]
            resp.result = text
            return resp.dict()


@command('/start')
def command_start(*args) -> dict:
    resp = BaseResponse()

    text = ''
    for name, f in commands.items():
        if name == 'start':
            continue
            
        text += f'/{name}: {f.__doc__}; '

    resp.result = text
    
    return resp.dict()
