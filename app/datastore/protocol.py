from typing import Protocol

from app.datastore.dataset import DataSet
from app.model.equipment import Equipment
from app.model.labo import Labo
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord
from app.model.user import User


class DataProvider(Protocol):
    @property
    def users(self) -> DataSet[User]:
        ...

    @property
    def equipments(self) -> DataSet[Equipment]:
        ...

    @property
    def reservations(self) -> DataSet[Reservation]:
        ...

    @property
    def usage_records(self) -> DataSet[UsageRecord]:
        ...

    @property
    def labos(self) -> DataSet[Labo]:
        ...


class DataManipulator(Protocol):
    def add_usage_record(self, usage_record: UsageRecord) -> None:
        ...

    def update_usage_record(self, usage_record: UsageRecord) -> None:
        ...

    def finish_usage_record(self, usage_record: UsageRecord) -> None:
        ...
