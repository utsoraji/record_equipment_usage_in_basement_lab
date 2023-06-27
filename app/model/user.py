import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from app.model.entity import Entity, RefId
from app.model.equipment import Equipment
from app.model.labo import Labo


class UserPosition(Enum):
    FACULTY = auto()
    STUDENT = auto()
    STAFF = auto()
    NONE = auto()

    @classmethod
    def value_of(cls, target_value):
        try:
            return cls[target_value]
        except ValueError:
            return cls.NONE


class UserRole(Enum):
    ADMIN = auto()
    USER = auto()
    NONE = auto()

    @classmethod
    def value_of(cls, target_value):
        try:
            return cls[target_value]
        except ValueError:
            return cls.NONE


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

    def is_expired(
        self, reference_date: datetime.datetime = datetime.datetime.now()
    ) -> bool:
        return self.expire_date is not None and self.expire_date <= reference_date

    @classmethod
    def unknown(cls, id: str | RefId) -> "User":
        return cls(
            id,
            "",
            f"Unknown ID:{id}",
            "",
        )
