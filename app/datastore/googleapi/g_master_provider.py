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
                UserPosition(record["position"]) if record["position"] else None,
                UserRole(record["role"]) if record["role"] else None,
                parse_licenses(record["licenses"]),
                conv_from_s_date(record["expire_date"])
                if record["expire_date"]
                else None,
            )
            for record in self._master_db["users"]
        ]
        return {user.id: user for user in list}

    @property
    def equipments(self) -> dict[RefId, Equipment]:
        list = [
            Equipment(
                RefId(record["id"]),
                record["name_roman"],
                record["name_kanakanji"],
                record["image_url"],
                record["location"],
                record["check_license"] if record["check_license"] else False,
            )
            for record in self._master_db["equipments"]
        ]
        return {eq.id: eq for eq in list}

    @property
    def labos(self) -> dict[RefId, Labo]:
        list = [
            Labo(record["id"], record["name_roman"], record["name_kanakanji"])
            for record in self._master_db["labos"]
        ]
        return {labo.id: labo for labo in list}
