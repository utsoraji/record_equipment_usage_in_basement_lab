import datetime
from dataclasses import dataclass

from app.model.entity import Entity
from app.model.equipment import Equipment
from app.model.user import User


@dataclass(frozen=True)
class Reservation(Entity):
    starting: datetime.datetime
    end: datetime.datetime
    user: User
    equipments: set[Equipment]
