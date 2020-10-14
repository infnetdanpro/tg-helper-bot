import asyncio
import itertools
import logging

from lib import telegram as tglib
from conf import config
from utils.functions import commands as bot_commands
from utils.serialization import serialize_response as serialize
from utils import command_parser


logging.basicConfig(level=logging.INFO)


async def main():
    tg = tglib.TelegramBot(token=config.TELEGRAM_BOT_TOKEN)

    offset = 0      # last update id
    for i in itertools.count(1):
        try:
            data: dict = await tg.get_updates(offset=offset)

            # Serialize data
            telegram_response = tg_resp = serialize(data.get('result', []))
            ready = bool(data['ok'])

            if tg_resp.results and ready:
                result = tg_resp.results[0]
                offset = result.update_id
                offset += 1
                
                last_chat_text = result.message.text
                last_chat_id = result.message.chat['id']
                last_chat_name = result.message.chat['first_name']

                command, message = command_parser.parse_user_message(last_chat_text)

                if command and command in bot_commands.keys():
                    f = bot_commands.get(command)
                    if f and f(message).get('result_type') == 'photo':
                        await tg.send_photo(params={'chat_id': last_chat_id, 'photo': f(message)['result']})
                    elif f and f(message).get('result_type') == 'text':
                        await tg.send_message(params={'chat_id': last_chat_id, 'text': f(message)['result']})
                else:
                    await tg.send_message(params={'chat_id': last_chat_id, 'text': 'Command not found'})

                logging.info('[%s]: [%s]', last_chat_name, last_chat_text)

        except Exception as e:
            logging.exception(e)

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
