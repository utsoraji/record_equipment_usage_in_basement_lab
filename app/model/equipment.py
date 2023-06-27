from dataclasses import dataclass
from typing import Optional

from app.model.entity import Entity, RefId


@dataclass(frozen=True)
class Equipment(Entity):
    name_roman: Optional[str]
    name_kanakanji: str
    image_id: str
    location: str
    check_license: bool = False

    @property
    def name(self) -> str:
        if self.name_roman is not None:
            return self.name_roman
        elif self.name_kanakanji is not None:
            return self.name_kanakanji
        raise ValueError("No name")

    @classmethod
    def unknown(cls, id: str | RefId) -> "Equipment":
        return cls(
            id,
            f"Unknown ID:{id}",
            "",
            "",
            "",
        )
