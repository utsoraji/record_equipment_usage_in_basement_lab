import datetime
from typing import Iterable, Iterator, TypeVar

from app.model.entity import Entity, RefId

T = TypeVar("T", bound=Entity)


class DataSet(Iterable[T]):
    def __init__(self, items: Iterable[T], id_attr: str = "id") -> None:
        self.items = {RefId(getattr(item, id_attr)): item for item in items}
        self._timestamp = datetime.datetime.now()

    def __iter__(self) -> Iterator[T]:
        return self.items.values().__iter__()

    def __getitem__(self, id: RefId) -> T:
        return self.as_dict()[id]

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp
