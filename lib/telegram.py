import aiohttp
import typing
from utils import functions
# Что я хочу от бота

# 1. Команды
# 2. По командам - функции
# 3. Стандарт ответа


COMMANDS = {name: getattr(functions, name).__doc__ for name in dir(functions) if not name.startswith('__')}


class TelegramBot:
    func_result: dict = {}

    def __init__(self, token):
        self.token: str = token
        self.API_URL: str = f'https://api.telegram.org/bot{self.token}/'

    def command_list(self) -> dict:
        """List of each function with docstring""" 
        return COMMANDS

    def generate_description(self) -> str:
        command_list = ''
        
        for command, about in COMMANDS.items():
            command_list += f""" * {command}: {about}"""

        text = f"""*Commands on this bot:*{command_list}"""
        return text


    async def run_function(self, func, *args, **kwargs):
        # TODO: standartize in future functions
        self.func_result = func(*args, **kwargs)
        return self.func_result

    # API
    async def get_updates(self, timeout: int = 30, offset: int = 0) -> dict:
        """Pull latest events from bot"""
        params = {'timeout': timeout}
        if offset:
            params['offset'] = offset
        query: str = self.API_URL + 'getUpdates'

        async with aiohttp.ClientSession() as session:
            async with session.get(query, params=params) as resp:
                print(resp.url)
                return await resp.json()

    async def send_message(self, params: dict) -> dict:
        """Send answer for messages
        chat_id (from): int
        text: str
        """
        query = self.API_URL + 'sendMessage'

        async with aiohttp.ClientSession() as session:
            async with session.get(query, params=params) as resp:
                return await resp.json()

    async def send_photo(self, params: dict) -> dict:
        """Send photo for messages
        chat_id (from): int
        text: str
        """
        query = self.API_URL + 'sendPhoto'

        async with aiohttp.ClientSession() as session:
            async with session.get(query, params=params) as resp:
                return await resp.json()