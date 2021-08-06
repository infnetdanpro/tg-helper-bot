from enum import Enum
from dataclasses import dataclass, asdict, field
from typing import List, Dict


ResultTypes = Enum('ResultTypes', ((s, s) for s in ('text', 'photo')))


@dataclass
class Base:
    def dict(self):
        return asdict(self)

    def __getattr__(self, name):
        if name.endswith('_'):
            return getattr(self, name[:-1])


@dataclass
class BaseResponse(Base):
    result_type: str = ResultTypes.text.value
    result: str = None


@dataclass
class TelegramMessageFrom(Base):
    id: int = 0
    is_bot: bool = False
    first_name: str = None
    last_name: str = None
    username: str = None
    language_code: str = None


@dataclass
class TelegramMessageChat(Base):
    id: int = 0
    first_name: str = None
    last_name: str = None
    username: str = None
    type: str = None


@dataclass
class TelegramMessage(Base):
    date: int = 0
    text: str = None
    message_id: int = 0
    entities: list = None   # [{"offset":0,"length":5,"type":"bot_command"}]
    from_: TelegramMessageFrom = field(default_factory=TelegramMessageFrom)
    chat: TelegramMessageChat = field(default_factory=TelegramMessageChat)


@dataclass
class TelegramEntity(Base):
    update_id: int = None
    message: TelegramMessage = field(default_factory=TelegramMessage)
    edited_message: TelegramMessage = field(default_factory=TelegramMessage)



@dataclass
class TelegramResponse(Base):
    results: List[TelegramEntity] = field(default_factory=TelegramEntity)
