from dataclasses import dataclass

from app.model.entity import Entity


@dataclass(frozen=True)
class Labo(Entity):
    name: str
