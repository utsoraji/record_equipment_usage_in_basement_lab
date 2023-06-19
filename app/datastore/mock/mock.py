import datetime
import time

from app.datastore.protocol import MasterProvider, TransactionController
from app.model.entity import RefId
from app.model.equipment import Equipment
from app.model.labo import Labo
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord
from app.model.user import User, UserPosition, UserRole

labos = [Labo(RefId("Labo1"), "Labo1", "ラボ1")]

users = [
    User(
        RefId("admin_id"),
        "xxx@example.com",
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
        "xxx@example.com",
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
        "xxx@example.com",
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
    Equipment(
        RefId("machine1"),
        "Machine1",
        "マシン1",
        "https://lh6.googleusercontent.com/ltNKndOusrdM9B1YKSySnDrKDMySfcUuugoYxxgAy1A83AiSjs-79gbSYa9AC1GWu7Z0co2WM0DBqmEVY7TXQYehPrd2Z-9f0DqQU8FWsaoN588o48BU6IHHqe7c6V2A0g=w1280",
        "008",
        False,
    ),
    Equipment(
        RefId("machine2"),
        "Machine2",
        "マシン2",
        "https://lh6.googleusercontent.com/ltNKndOusrdM9B1YKSySnDrKDMySfcUuugoYxxgAy1A83AiSjs-79gbSYa9AC1GWu7Z0co2WM0DBqmEVY7TXQYehPrd2Z-9f0DqQU8FWsaoN588o48BU6IHHqe7c6V2A0g=w1280",
        "008",
        False,
    ),
    Equipment(
        RefId("machine3"),
        "Machine3",
        "マシン3",
        "https://lh6.googleusercontent.com/ltNKndOusrdM9B1YKSySnDrKDMySfcUuugoYxxgAy1A83AiSjs-79gbSYa9AC1GWu7Z0co2WM0DBqmEVY7TXQYehPrd2Z-9f0DqQU8FWsaoN588o48BU6IHHqe7c6V2A0g=w1280",
        "008",
        False,
    ),
    Equipment(
        RefId("machine4"),
        "Machine4",
        "マシン4",
        "https://lh6.googleusercontent.com/ltNKndOusrdM9B1YKSySnDrKDMySfcUuugoYxxgAy1A83AiSjs-79gbSYa9AC1GWu7Z0co2WM0DBqmEVY7TXQYehPrd2Z-9f0DqQU8FWsaoN588o48BU6IHHqe7c6V2A0g=w1280",
        "014",
        False,
    ),
    Equipment(
        RefId("m_req_license"),
        "Require license",
        "要免許",
        "https://lh3.googleusercontent.com/EjCto8WsmVrtrO5NICi9JUDZ0iJnrNWAu9eaebnL4Dm2KXgdoZosu1XpFuBe9-kU61NvjEzjh0DG2xt1Bmv4E9MjkKXPJIlK1gB1RT3GUU-EFv5J1NFvMxawtl5EB1lIpQ=w1280",
        "014",
        True,
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
        {equipments[0]},
    ),
    UsageRecord(
        "2",
        datetime.datetime.now(),
        datetime.datetime.now() + datetime.timedelta(hours=3),
        None,
        users[0],
        {equipments[0], equipments[1]},
    ),
]


class MockMasterProvider(MasterProvider):
    @property
    def users(self) -> dict[RefId, User]:
        return {user.id: user for user in users}

    @property
    def equipments(self) -> dict[RefId, Equipment]:
        return {equipment.id: equipment for equipment in equipments}

    @property
    def labos(self) -> dict[RefId, Labo]:
        return {labo.id: labo for labo in labos}


class MockTransactionController(TransactionController):
    @property
    def reservations(self) -> dict[RefId, Reservation]:
        return dict()

    @property
    def usage_records(self) -> dict[RefId, UsageRecord]:
        return {usage_record.id: usage_record for usage_record in usage_records}

    def add_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        time.sleep(1)
        return usage_record

    def finish_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        time.sleep(1)
        return usage_record
