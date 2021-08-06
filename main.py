import asyncio
import itertools
import logging

from lib import telegram as tglib
from conf import config
from utils.functions import commands as bot_commands
from utils.serialization import serialize_response as serialize
from utils import command_parser


tg_app = tglib.TelegramBot(token=config.TELEGRAM_BOT_TOKEN)
logging.basicConfig(level=logging.INFO)


async def send_response(command: str, message: str, function, chat_id: int):
    """
    Dynamic choose function for send response to user (result of functions)
    """
    response = {
        'chat_id': chat_id, 
        'text': 'Command not found'
    }
    
    if not function:
        return await tg_app.send_message(response)
    

    send_type = {
        'photo': tg_app.send_photo, 
        'text': tg_app.send_message
    }
    # do some work
    result = function(message)    
    
    result_type = result['result_type']
    response[result['result_type']] = result['result']
    if function.__name__.endswith('cmd'):
        response['parse_mode'] = 'MarkdownV2'
    # Send typed response
    await send_type[result_type](params=response)



async def main():
    offset = 0      # last update id
    for i in itertools.count(1):
        data: dict = await tg_app.get_updates(offset=offset)

        # Serialize data
        tg_resp = serialize(data.get('result', []))

        ready = bool(data['ok'])
        
        if tg_resp.results and ready:
            result = tg_resp.results[0]
            offset = result.update_id
            offset += 1
            result = result.dict()          
            last_chat_text = result['message']['text']
            last_chat_id = result['message']['chat']['id']
            last_chat_name = result['message']['chat']['username']

            command, message = command_parser.parse_user_message(last_chat_text)
            if not message:
                continue
            await send_response(command, message, bot_commands.get(command), last_chat_id)

            logging.info('[%s]: [%s]', last_chat_name, last_chat_text)

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
