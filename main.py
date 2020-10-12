import asyncio
import itertools
import logging

from lib import telegram as tglib
from conf import config
from utils.functions import commands as bot_commands
from utils import command_parser


async def main():
    tg = tglib.TelegramBot(token=config.TELEGRAM_BOT_TOKEN)

    offset = 0      # last update id
    for i in itertools.count(1):
        try:
            data: dict = await tg.get_updates(offset=offset)

            result = data.get('result', [])
            ready = bool(data['ok'])

            if result and ready:
                result = result[0]
                offset = result['update_id']
                offset += 1

                # {'update_id': 646755242, 'message': {'message_id': 926, 'from': {'id': 116910426, 'is_bot': False, 'first_name': 'Максим', 'last_name': 'Артемьев', 'username': 'max_artemev', 'language_code': 'ru'}, 'chat': {'id': 116910426, 'first_name': 'Максим', 'last_name': 'Артемьев', 'username': 'max_artemev', 'type': 'private'}, 'date': 1602274349, 'text': '/bad_harry', 'entities': [{'offset': 0, 'length': 10, 'type': 'bot_command'}]}}

                last_chat_text = result['message']['text']
                last_chat_id = result['message']['chat']['id']
                last_chat_name = result['message']['chat']['first_name']

                command, message = command_parser.parse_user_message(last_chat_text)

                if command and command in bot_commands.keys():
                    f = bot_commands.get(command)
                    if f and f(message).get('result_type') == 'photo':
                        await tg.send_photo(params={'chat_id': last_chat_id, 'photo': f(message)['result']})
                    elif f and f(message).get('result_type') == 'text':
                        await tg.send_message(params={'chat_id': last_chat_id, 'text': f(message)['result']})
                elif command == 'start':
                    await tg.send_message(params={'chat_id': last_chat_id, 'text': '`/cats /bad_harry`', 'parse_mode': 'MarkdownV2'})
                else:
                    await tg.send_message(params={'chat_id': last_chat_id, 'text': 'Command not found'})
        except Exception as e:
            logging.warning(e)

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
