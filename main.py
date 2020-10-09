import asyncio
from lib import telegram as tglib
from conf import config
from utils.functions import *
from utils import command_parser


async def main():
    tg = tglib.TelegramBot(token=config.TELEGRAM_BOT_TOKEN)

    commands: dict = tg.command_list()

    offset = 0      # last update id
    while True:
        data: dict = await tg.get_updates(offset=offset)

        result = data.get('result', [])
        ready = bool(data['ok'])

        if result and ready:
            result = result[0]
            offset = result['update_id']
            offset += 1

            last_chat_text = result['message']['text']
            last_chat_id = result['message']['chat']['id']
            last_chat_name = result['message']['chat']['first_name']

            command, message = command_parser.parse_user_message(last_chat_text)

            if command and command in commands.keys():
                f = globals().get(command)
                if f and f(message).get('result_type') == 'photo':
                    await tg.send_photo(params={'chat_id': last_chat_id, 'photo': f(message)['result']})
                elif f and f(message).get('result_type') == 'text':
                    await tg.send_message(params={'chat_id': last_chat_id, 'text': f(message)['result']})
            elif command == 'start':
                await tg.send_message(params={'chat_id': last_chat_id, 'text': '`/cats /bad_harry`', 'parse_mode': 'MarkdownV2'})
            else:
                await tg.send_message(params={'chat_id': last_chat_id, 'text': 'Command not found'})

            print(f'[{last_chat_name}]: [{last_chat_text}]')

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
