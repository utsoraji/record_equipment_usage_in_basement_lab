from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RefId:
    id: str

    def __str__(self) -> str:
        return self.id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RefId) and self.id == other.id


@dataclass(frozen=True)
class Entity(Protocol):
    id: RefId
