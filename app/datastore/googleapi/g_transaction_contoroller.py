import datetime
import uuid

import appconfig
from app.datastore.googleapi.credential import connect_gspread
from app.datastore.googleapi.spreadsheet_proxy import SpreadsheetProxy
from app.datastore.googleapi.utils import (
    convert_from_serial_datetime,
    convert_to_serial_datetime,
    parse_equipments,
    parse_equipments_reservation,
)
from app.datastore.protocol import MasterProvider, NewUsageRecord, TransactionController
from app.model.entity import RefId
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord

DELTA_HOUR = datetime.timedelta(hours=1)


def elapsed_by_hour(dt: datetime.datetime) -> float:
    return (datetime.datetime.now() - dt) / DELTA_HOUR


class GoogleTransactionController(TransactionController):
    def __init__(
        self,
        master_provider: MasterProvider,
    ):
        self._master_provider = master_provider
        print(appconfig.TRANSACTION_SPREADSHEET_KEY)
        print(appconfig.RESERVATION_SPREADSHEET_KEY)
        self._transaction_db = SpreadsheetProxy(
            connect_gspread(), appconfig.TRANSACTION_SPREADSHEET_KEY
        )
        self._resavation_db = SpreadsheetProxy(
            connect_gspread(), appconfig.RESERVATION_SPREADSHEET_KEY
        )

    @property
    def usage_records(self) -> dict[RefId, UsageRecord]:
        list = [
            UsageRecord(
                RefId(record["id"]),
                starting=convert_from_serial_datetime(record["starting"]),
                end_estimate=convert_from_serial_datetime(record["end_estimate"]),
                end_actual=convert_from_serial_datetime(record["end_actual"]),
                user=self._master_provider.get_user(record["user"]),
                equipments=[
                    self._master_provider.get_equipment(eq_id)
                    for eq_id in parse_equipments(record["equipments"])
                ],
                note=record["note"],
            )
            for record in self._transaction_db["usage_records"]
        ]

        return {record.id: record for record in list}

    @property
    def reservations(self) -> dict[RefId, Reservation]:
        if elapsed_by_hour(self._resavation_db.last_loaded_at) > 6:
            self._resavation_db.reload()
        list = [
            Reservation(
                id=RefId(record["イベントID"]),
                starting=convert_from_serial_datetime(record["使用開始日時/Start time"]),
                end=convert_from_serial_datetime(record["使用終了日時/End time"]),
                user=self._master_provider.get_user(record["メールアドレス"]),
                equipments=[
                    self._master_provider.get_equipment(eq_name)
                    for eq_name in parse_equipments_reservation(record["装置名/Equipment"])
                ],
            )
            for record in self._resavation_db["フォームの回答 1"]
            if record["イベントID"] != "error"
        ]
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        list = filter(
            lambda r: isinstance(r.starting, datetime.datetime) and r.starting > today,
            list,
        )

        return {record.id: record for record in list}

    def add_usage_record(self, new_record: NewUsageRecord) -> UsageRecord:
        print("aaa")
        record = UsageRecord(
            id=RefId(uuid.uuid4().hex),
            starting=new_record.starting,
            user=new_record.user,
            equipments=new_record.equipments,
            note=new_record.note,
        )

        row: dict = {
            "id": str(record.id),
            "starting": convert_to_serial_datetime(record.starting),
            "user": str(record.user.id),
            "equipments": ",".join(
                str(equipment.id) for equipment in record.equipments
            ),
            "note": record.note,
        }
        print(row)

        self._transaction_db["usage_records"].append_row(row)
        self._transaction_db.reload()
        return record

    def finish_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        self._transaction_db["history"].append_row(
            {
                "id": str(usage_record.id),
                "user": str(usage_record.user.id),
                "equipments": ",".join(
                    str(equipment.id) for equipment in usage_record.equipments
                ),
                "starting": convert_to_serial_datetime(usage_record.starting),
                "end_actual": convert_to_serial_datetime(usage_record.end_actual),
                "note": usage_record.note,
            }
        )
        self._transaction_db["usage_records"].delete_row({"id": usage_record.id})

        self._transaction_db.reload()
        return usage_record
