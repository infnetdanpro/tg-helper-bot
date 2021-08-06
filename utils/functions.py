# This file include function by name
import os
import subprocess
import requests
import itertools

from random import randint
from conf import config
from models.response import BaseResponse, ResultTypes


commands = {}

def command(command_name): 
    def wrap(f): 
        commands[command_name[1:]] = f
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

@command('/start')
def command_start(*args) -> dict:
    print('11111111111111')
    resp = BaseResponse()

    text = ''
    for name, f in commands.items():
        if name == 'start':
            continue

        text += f'/{name}: {f.__doc__}; '

    resp.result = text
    
    return resp.dict()


@command('/ngrok')
def command_cmd(password) -> dict:
    """ Run ngrok tunnel on server: password"""
    resp = BaseResponse()
    
    if password != '82828asdkja':
        resp.result = 'Bad authorization'
        return resp.dict()
    try:
        r = requests.get('http://127.0.0.1:4040/api/tunnels')
        resp.result = str(r.json()['tunnels'][0]['public_url'])
    except Exception as e:
        resp.result = str(e)

    return resp.dict()


