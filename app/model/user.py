import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from app.model.entity import Entity
from app.model.equipment import Equipment
from app.model.labo import Labo


class UserPosition(Enum):
    FACULTY = auto()
    STUDENT = auto()
    STAFF = auto()
    NONE = auto()


class UserRole(Enum):
    ADMIN = auto()
    USER = auto()
    NONE = auto()


@dataclass(frozen=True)
class User(Entity):
    ecc_mail: str
    name_roman: str
    name_kanakanji: str
    labo: Labo = None
    position: UserPosition = UserPosition.NONE
    role: UserRole = UserRole.NONE
    licenses: set[Equipment] = ()
    expire_date: Optional[datetime.date] = None

    @property
    def name(self) -> str:
        if self.name_roman is not None and self.name_roman != "":
            return self.name_roman
        elif self.name_kanakanji is not None and self.name_kanakanji != "":
            return self.name_kanakanji
        else:
            return f"ID: {self.id}"

    def validate(self) -> None:
        return super().validate()

    @classmethod
    def empty(cls) -> "User":
        return cls(
            "-",
            "-",
            "-",
            "-",
            licenses=[],
            expire_date=None,
        )
