import datetime

import appconfig
from app.datastore.googleapi.credential import connect_gspread
from app.datastore.googleapi.spreadsheet_proxy import SpreadsheetProxy
from app.datastore.googleapi.utils import (
    convert_from_serial_datetime as conv_from_s_date,
)
from app.datastore.protocol import MasterProvider
from app.model.entity import RefId
from app.model.equipment import Equipment
from app.model.labo import Labo
from app.model.user import User, UserPosition, UserRole


class GoogleMasterProvider(MasterProvider):
    def __init__(self):
        gspread_client = connect_gspread()
        self._master_db = SpreadsheetProxy(
            gspread_client, appconfig.MASTER_SPREADSHEET_KEY
        )
        pass

    def _to_refId(self, id: str | RefId) -> RefId:
        if isinstance(id, RefId):
            return id
        if isinstance(id, str):
            return RefId(id)
        if id is None:
            return None
        raise ValueError(f"Invalid id type: {type(id)}")

    @property
    def users(self) -> dict[RefId, User]:
        def parse_licenses(licenses: str | None) -> set[Equipment]:
            if licenses is None:
                return set()
            return set(self.equipments[id.strip()] for id in licenses.split(","))

        list = [
            User(
                RefId(record["id"]),
                record["ecc_mail"],
                record["name_roman"],
                record["name_kanakanji"],
                self.labos[record["labo"]] if record["labo"] else None,
                UserPosition.value_of(record.get("position")),
                UserRole.value_of(record.get("role")),
                parse_licenses(record["licenses"]),
                conv_from_s_date(record.get("expire_date")),
            )
            for record in self._master_db["users"]
        ]

        return {user.id: user for user in list if not user.is_expired()}

    def get_user(self, user_id: RefId | str) -> User:
        id = self._to_refId(user_id)
        return self.users.get(id, User.unknown(id))

    @property
    def equipments(self) -> dict[RefId, Equipment]:
        list = [
            Equipment(
                RefId(record["id"]),
                record["name_roman"],
                record["name_kanakanji"],
                record["image_id"],
                record["location"],
                record["check_license"] if record["check_license"] else False,
            )
            for record in self._master_db["equipments"]
        ]
        return {eq.id: eq for eq in list}

    def get_equipment(self, eq_id: RefId | str) -> Equipment:
        id = self._to_refId(eq_id)
        return self.equipments.get(id, Equipment.unknown(id))

    @property
    def labos(self) -> dict[RefId, Labo]:
        list = [
            Labo(record["id"], record["name_roman"], record["name_kanakanji"])
            for record in self._master_db["labos"]
        ]
        return {labo.id: labo for labo in list}

    def get_labo(self, labo_id: RefId | str) -> Labo:
        id = self._to_refId(labo_id)
        return self.labos.get(id, Labo.unknown(id))
