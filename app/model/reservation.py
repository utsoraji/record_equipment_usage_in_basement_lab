import datetime
from dataclasses import dataclass

from app.model.entity import Entity, RefId


@dataclass(frozen=True)
class Reservation(Entity):
    starting: datetime.datetime
    end: datetime.datetime
    user: RefId
    equipment: RefId
