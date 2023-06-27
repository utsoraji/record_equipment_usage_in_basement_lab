from dataclasses import dataclass
from typing import Optional

from app.model.entity import Entity, RefId


@dataclass(frozen=True)
class Labo(Entity):
    name_roman: Optional[str]
    name_kanakanji: Optional[str]

    @property
    def name(self) -> str:
        if self.name_roman is not None and self.name_roman != "":
            return self.name_roman
        elif self.name_kanakanji is not None and self.name_kanakanji != "":
            return self.name_kanakanji
        else:
            return f"ID: {self.id}"

    @classmethod
    def unknown(cls, id: str | RefId) -> "Labo":
        return cls(
            id,
            f"Unknown ID:{id}",
            "",
        )
