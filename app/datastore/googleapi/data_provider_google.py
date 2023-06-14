import datetime

import appconfig
from app.const import UserPosition, UserRole
from app.datastore.dataset import DataSet
from app.datastore.googleapi.credential import connect_gspread
from app.datastore.googleapi.spreadsheet_as_db import SpreadsheetAsDataBase
from app.datastore.protocol import MasterProvider
from app.model.entity import RefId
from app.model.equipment import Equipment
from app.model.labo import Labo
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord
from app.model.user import User


class GoogleDataProvider(MasterProvider):
    def __init__(self):
        gspread_client = connect_gspread()
        self._master_db = SpreadsheetAsDataBase(
            gspread_client, appconfig.MASTER_SPREADSHEET_KEY
        )
        pass

    @property
    def users(self) -> DataSet[User]:
        def parse_licenses(licenses: str) -> set[Equipment]:
            return set(self.equipments[id.strip()] for id in licenses.split(","))

        list = [
            User(
                RefId(record["ecc_mail"]),
                record["ecc_mail"],
                record["name_roman"],
                record["name_kanakanji"],
                self.labos[record["labo_id"]],
                UserPosition(record["user_position"]),
                UserRole(record["user_role"]),
                parse_licenses(record["licenses"]),
                datetime.date(record["expire_date"]),
            )
            for record in self._master_db["user"]
        ]
        return DataSet(list)

    @property
    def equipments(self) -> DataSet[Equipment]:
        list = [
            Equipment(
                RefId(record["id"]),
                record["name_roman"],
                record["name_kanakanji"],
                record["image_url"],
                self.labos[record["labo_id"]],
                record["location"],
                bool(record["check_license"]),
            )
            for record in self._master_db["equipment"]
        ]
        return DataSet(list)

    @property
    def reservations(self) -> DataSet[Reservation]:
        ...

    @property
    def usage_records(self) -> DataSet[UsageRecord]:
        ...

    @property
    def labos(self) -> DataSet[Labo]:
        list = [
            Labo(record["id"], record["name"]) for record in self._master_db["labo"]
        ]
        return DataSet(list)
