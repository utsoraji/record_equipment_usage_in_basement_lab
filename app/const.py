from enum import Enum, auto


class PageId(Enum):
    START = auto()
    ENTRY = auto()
    USE_START = auto()
    USE_FINISH = auto()
    USE_RESPONSE = auto()


class SessionKey(Enum):
    APP = auto()
    IS_INITIALIZED = auto()
    TO_BE_RESTART = auto()
    CONTEXT = auto()
    SERVICES = auto()
