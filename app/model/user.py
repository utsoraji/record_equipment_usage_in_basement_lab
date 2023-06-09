import datetime
from dataclasses import dataclass

from app.const import UserPosition, UserRole
from app.model.entity import Entity, RefId


@dataclass(frozen=True)
class User(Entity):
    name_roman: str
    name_kanakanji: str
    labo: RefId = None
    position: UserPosition = UserPosition.NONE
    role: UserRole = UserRole.NONE
    licenses: tuple[RefId] = ()
    expire_date: datetime.date = None

    @property
    def name(self) -> str:
        if self.name_roman is not None and self.name_roman != "":
            return self.name_roman
        elif self.name_kanakanji is not None and self.name_kanakanji != "":
            return self.name_kanakanji
        else:
            return f"ID: {self.id}"

    @classmethod
    def empty(cls) -> "User":
        return cls(
            "-",
            "-",
            "-",
            licenses=[],
            expire_date=None,
        )
