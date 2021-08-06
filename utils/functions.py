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


# @command('/cats')
# def command_random_cats(search_query: str = 'cats') -> dict:
#    """Get random cats"""
#    resp = BaseResponse()
#
#    headers = {'Authorization': config.PEXELS_IMAGE_API_TOKEN}
#    params = {'query': search_query or 'cats', 'page': randint(1,2852), 'per_page': 1}
#
#    r = requests.get(url=config.PEXELS_IMAGE_API_URL, params=params, headers=headers)
#    data: dict = r.json()
    
#    if r.status_code == 200 and data:
#        resp.result_type = ResultTypes.photo.value
#        resp.result = data['photos'][-1]['src']['large']
#    
#    return resp.dict()


@command('/echo')
def command_echo(text: str) -> dict:
    """Test echo function"""
    resp = BaseResponse()
    resp.result = text

    return resp.dict()

@command('/start')
def command_start(*args) -> dict:
    resp = BaseResponse()

    text = ''
    for name, f in commands.items():
        if name == 'start':
            continue

        text += f"""/{name}: {f.__doc__};
"""

    resp.result = text
    
    return resp.dict()


@command('/public_domain')
def command_domain(*args, **kwargs) -> dict:
    """ Show public domain for server"""
    resp = BaseResponse()
    try:
        r = requests.get('http://127.0.0.1:4040/api/tunnels')
        resp.result = str(r.json()['tunnels'][0]['public_url'])
    except Exception as e:
        resp.result = str(e)

    return resp.dict()


@command('/cmd')
def command_cmd(*args):
    """ Server console"""
    resp = BaseResponse()
    params = list(args)[0].split(' ')
    auth = params.pop(0)
    if auth == config.AUTH:
        try:
            r = subprocess.check_output(params)
            resp.result = f"""```{r.decode('utf-8')}```"""
        except Exception as e:
            resp.result = str(e)
        return resp.dict()

    resp.result = 'Wrong auth'
    return resp.dict()


