import aiohttp
import typing


class TelegramBot:
    func_result: dict = {}

    def __init__(self, token):
        self.token: str = token
        self.API_URL: str = f'https://api.telegram.org/bot{self.token}/'

    async def do_request(self, query: str, params: dict = None) -> dict:
        if not params:
            params = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(query, params=params) as resp:
                return await resp.json()


    async def run_function(self, func, *args, **kwargs):
        # TODO: standartize in future functions
        self.func_result = func(*args, **kwargs)
        return self.func_result

    async def get_updates(self, timeout: int = 30, offset: int = 0) -> dict:
        """Pull latest events from bot"""
        params = {'timeout': timeout}
        if offset:
            params['offset'] = offset
        query: str = self.API_URL + 'getUpdates'
        return await self.do_request(query, params)

    async def send_message(self, params: dict) -> dict:
        """Send answer for messages
        chat_id (from): int
        text: str
        """
        query = self.API_URL + 'sendMessage'
        return await self.do_request(query, params)

    async def send_photo(self, params: dict) -> dict:
        """Send photo for messages
        chat_id (from): int
        text: str
        """
        query = self.API_URL + 'sendPhoto'
        return await self.do_request(query, params)
