from models.response import TelegramResponse, TelegramEntity, TelegramMessage


def serialize_response(results: []) -> TelegramResponse:
    telegram_response = TelegramResponse(results=[TelegramEntity(**row) for row in results])

    for i, row in enumerate(telegram_response.results):
        row.message['from_'] = row.message.pop('from')
        telegram_response.results[i].message = TelegramMessage(**row.message)
    return telegram_response
