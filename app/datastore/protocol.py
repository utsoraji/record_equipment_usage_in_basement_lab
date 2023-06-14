import datetime
from dataclasses import dataclass
from typing import Optional, Protocol

from app.datastore.dataset import DataSet
from app.model.equipment import Equipment
from app.model.labo import Labo
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord
from app.model.user import User


class MasterProvider(Protocol):
    @property
    def users(self) -> DataSet[User]:
        ...

    @property
    def equipments(self) -> DataSet[Equipment]:
        ...

    @property
    def labos(self) -> DataSet[Labo]:
        ...


@dataclass(frozen=True)
class NewUsageRecord:
    user: User
    equipments: set[Equipment]
    starting: datetime.datetime
    end_estimate: Optional[datetime.datetime]


class TransactionController(Protocol):
    @property
    def reservations(self) -> DataSet[Reservation]:
        ...

    @property
    def usage_records(self) -> DataSet[UsageRecord]:
        ...

    def add_usage_record(self, usage_record: NewUsageRecord) -> UsageRecord:
        ...

    def update_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        ...

    def finish_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        ...
