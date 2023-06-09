from dataclasses import dataclass

from app.model.entity import Entity, RefId


@dataclass(frozen=True)
class Equipment(Entity):
    name_roman: str
    name_kanakanji: str
    labo: RefId
    location: str
    check_license: bool

    @property
    def name(self) -> str:
        if self.name_roman is not None:
            return self.name_roman
        elif self.name_kanakanji is not None:
            return self.name_kanakanji
        raise ValueError("No name")
