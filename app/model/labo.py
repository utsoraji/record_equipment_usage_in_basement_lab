from dataclasses import dataclass
from typing import Optional

from app.model.entity import Entity


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

    def validate(self) -> None:
        return super().validate()
