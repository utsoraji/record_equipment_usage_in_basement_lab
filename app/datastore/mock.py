import datetime

from app.const import UserPosition, UserRole
from app.datastore.protocol import DataManipulator, DataProvider, DataSet
from app.model.entity import RefId
from app.model.equipment import Equipment
from app.model.labo import Labo
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord
from app.model.user import User

labos = [Labo(RefId("Labo1"), "Labo1")]

users = [
    User(
        RefId("admin_id"),
        "Admin",
        "アドミン",
        labos[0].id,
        UserPosition.STAFF,
        UserRole.ADMIN,
        (),
        None,
    ),
    User(
        RefId("student1"),
        "",
        "学生1",
        labos[0].id,
        UserPosition.STUDENT,
        UserRole.USER,
        (),
        None,
    ),
    User(
        RefId("student2"),
        "Student2",
        "",
        labos[0].id,
        UserPosition.STUDENT,
        UserRole.USER,
        (RefId("m_req_license"),),
        None,
    ),
]

equipments = [
    Equipment(RefId("machine"), "Machine", "マシン", labos[0].id, "008", False),
    Equipment(
        RefId("m_req_license"), "Require license", "要免許", labos[0].id, "008", True
    ),
]

reservations = []

usage_records = [
    UsageRecord(
        "1",
        datetime.datetime.now(),
        datetime.datetime.now() + datetime.timedelta(hours=3),
        None,
        users[0],
        equipments[0],
    ),
    UsageRecord(
        "2",
        datetime.datetime.now(),
        datetime.datetime.now() + datetime.timedelta(hours=3),
        None,
        users[0],
        equipments[0],
    ),
]


class MockDataProvider(DataProvider):
    @property
    def users(self) -> DataSet[User]:
        return DataSet(users, "id")

    @property
    def equipments(self) -> DataSet[Equipment]:
        return DataSet(equipments, "name_roman")

    @property
    def reservations(self) -> DataSet[Reservation]:
        return []

    @property
    def usage_records(self) -> DataSet[UsageRecord]:
        return DataSet(usage_records, "id")

    @property
    def labos(self) -> DataSet[Labo]:
        return DataSet(labos, "name")


class MockDataManipulator(DataManipulator):
    def add_usage_record(self, usage_record: UsageRecord) -> None:
        pass

    def update_usage_record(self, usage_record: UsageRecord) -> None:
        pass

    def finish_usage_record(self, usage_record: UsageRecord) -> None:
        pass
