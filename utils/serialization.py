from models.response import TelegramResponse, TelegramEntity, TelegramMessage, TelegramMessageChat


def serialize_response(results: []) -> TelegramResponse:
    telegram_response = TelegramResponse(results=[TelegramEntity(**row) for row in results])

    for i, row in enumerate(telegram_response.results):
        row.message['from_'] = row.message.pop('from')
        message = TelegramMessage(**row.message)
        message.chat = TelegramMessageChat(**message.chat)
        telegram_response.results[i].message = message

    return telegram_response
