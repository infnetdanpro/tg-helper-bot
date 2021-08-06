import typing
from typing import AnyStr, Tuple, Union, List


def parse_user_message(user_message: AnyStr = None) -> Union[Tuple[AnyStr, AnyStr], Tuple[AnyStr, None]]:
    """Parsing string with message and split
    
    :user_message: string like '/echo text'
    @return: tuple with command/message
    """

    command, text = None, ' '

    if not user_message:
        return command, text
    
    user_message: List[AnyStr, AnyStr] = user_message.split(' ')
    
    try:
        # Cut first symbol '/' from command
        if len(user_message) == 1:
            command = user_message[0][1:] if user_message[0].startswith('/') else user_message[0]
            return command, text
        command, text = user_message.pop(0)[1:], ' '.join(user_message)

    except Exception as e:
        # TODO: add logging
        pass
    
    return command, text
