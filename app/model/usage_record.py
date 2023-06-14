import datetime
from dataclasses import dataclass
from typing import Optional

from app.model.entity import Entity
from app.model.equipment import Equipment
from app.model.user import User


@dataclass(frozen=True)
class UsageRecord(Entity):
    starting: datetime.datetime
    end_estimate: Optional[datetime.datetime]
    end_actual: Optional[datetime.datetime]
    user: User
    equipments: set[Equipment]
    note: Optional[str] = None

    def validate(self) -> None:
        return super().validate()
