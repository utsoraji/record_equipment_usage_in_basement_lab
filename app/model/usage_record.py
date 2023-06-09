import datetime
from dataclasses import dataclass

from app.model.entity import Entity, RefId


@dataclass(frozen=True)
class UsageRecord(Entity):
    starting: datetime.datetime
    end_estimate: datetime.datetime
    end_actual: datetime.datetime
    user: RefId
    equipment: RefId
    note: str = None
