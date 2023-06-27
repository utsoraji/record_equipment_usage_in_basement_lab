import datetime
from dataclasses import dataclass
from typing import Optional

from app.model.entity import Entity
from app.model.equipment import Equipment
from app.model.user import User


@dataclass(frozen=True)
class UsageRecord(Entity):
    user: User
    equipments: set[Equipment]
    starting: datetime.datetime
    end_estimate: Optional[datetime.datetime] = None
    end_actual: Optional[datetime.datetime] = None
    note: Optional[str] = None
