import datetime
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, Protocol

from app.model.entity import RefId
from app.model.equipment import Equipment
from app.model.labo import Labo
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord
from app.model.user import User


class StaticResourceProvider(Protocol):
    def get_image(self, id: str) -> BytesIO | str:
        """
        Returns either a BytesIO object or a url representing the image corresponding to the given ID.

        :param id: The ID of the image.
        :type id: str

        :return: Either a BytesIO object representing the image or a url for the image.
        :rtype: BytesIO | str
        """
        ...


class MasterProvider(Protocol):
    """
    Provide master data.
    """

    @property
    def users(self) -> dict[RefId, User]:
        ...

    def get_user(self, id: RefId | str) -> User:
        ...

    @property
    def equipments(self) -> dict[RefId, Equipment]:
        ...

    def get_equipment(self, id: RefId | str) -> Equipment:
        ...

    @property
    def labos(self) -> dict[RefId, Labo]:
        ...

    def get_labo(self, id: RefId | str) -> Labo:
        ...


@dataclass(frozen=True)
class NewUsageRecord:
    """
    Subset of UsageRecord to be added to backend datastore.
    """

    user: User
    equipments: set[Equipment]
    starting: datetime.datetime
    end_estimate: Optional[datetime.datetime] = None
    note: Optional[str] = None


class TransactionController(Protocol):
    """
    Provide transactional data and modify methods.
    """

    @property
    def reservations(self) -> dict[RefId, Reservation]:
        """
        Returns reservation dataset from source.\n
        The dataset includes only reservations that are on today.
        """
        ...

    @property
    def usage_records(self) -> dict[RefId, UsageRecord]:
        """
        Returns usage record dataset.\n
        The dataset includes only usage records that are not finished.
        """
        ...

    def add_usage_record(self, usage_record: NewUsageRecord) -> UsageRecord:
        """
        Adds a new usage record to backend datastore.

        :param usage_record: An instance of NewUsageRecord containing the data
                              of the usage to be added.
        :type usage_record: NewUsageRecord
        :return: An instance of UsageRecord containing the data of the added
                 usage.
        :rtype: UsageRecord
        """
        ...

    def finish_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        ...
