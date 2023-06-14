from dataclasses import dataclass
from typing import Optional

from app.model.entity import Entity
from app.model.labo import Labo


@dataclass(frozen=True)
class Equipment(Entity):
    name_roman: Optional[str]
    name_kanakanji: str
    image_url: str
    labo: Labo
    location: str
    check_license: bool

    @property
    def name(self) -> str:
        if self.name_roman is not None:
            return self.name_roman
        elif self.name_kanakanji is not None:
            return self.name_kanakanji
        raise ValueError("No name")

    def validate(self) -> None:
        return super().validate()
