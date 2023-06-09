from enum import Enum, auto


class PageId(Enum):
    START = auto()
    ENTRY = auto()
    USE_START = auto()
    USE_FINISH = auto()


class SessionKey(Enum):
    CURRENT_PAGE = auto()
    CURRENT_USER = auto()
    CONTEXT = auto()
    DATA_PROVIDER = auto()
    DATA_MANIPULATOR = auto()


class ContextKey(Enum):
    USAGE_RECORD = auto()


class UserPosition(Enum):
    FACULTY = auto()
    STUDENT = auto()
    STAFF = auto()
    NONE = auto()


class UserRole(Enum):
    ADMIN = auto()
    USER = auto()
    NONE = auto()
