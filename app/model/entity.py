from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RefId:
    id: str

    def __str__(self) -> str:
        return self.id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RefId) and self.id == other.id


@dataclass(frozen=True)
class Entity(ABC):
    id: RefId

    @abstractmethod
    def validate(self) -> None:
        ...
