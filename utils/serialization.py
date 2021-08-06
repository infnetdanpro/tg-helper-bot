from models.response import TelegramResponse, TelegramEntity, TelegramMessage, TelegramMessageChat


def serialize_response(results: []) -> TelegramResponse:
    """
    Serializing response from telegram API to Dataclass objects
    """
    telegram_response = TelegramResponse(results=[TelegramEntity(**row) for row in results])

    for i, row in enumerate(telegram_response.results):
        if row.edited_message:
            continue

        if row and row.message and row.message.get('from'):
            row.message['from_'] = row.message.pop('from')
        message = TelegramMessage(**row.message)
        message.chat = TelegramMessageChat(**message.chat)
        telegram_response.results[i].message = message

    return telegram_response
