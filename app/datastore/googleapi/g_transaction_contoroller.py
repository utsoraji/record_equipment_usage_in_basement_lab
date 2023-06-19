import appconfig
from app.datastore.googleapi.credential import connect_gspread
from app.datastore.googleapi.spreadsheet_proxy import SpreadsheetProxy
from app.datastore.protocol import DataSet, MasterProvider, TransactionController
from app.model.entity import RefId
from app.model.reservation import Reservation
from app.model.usage_record import UsageRecord


class GoogleTransactionController(TransactionController):
    def __init__(
        self,
        master_provider: MasterProvider,
    ):
        self._master_provider = master_provider
        self._transaction_db = SpreadsheetProxy(
            connect_gspread(), appconfig.TRANSACTION_SPREADSHEET_KEY
        )

    @property
    def usage_records(self) -> dict[RefId, UsageRecord]:
        self._transaction_db["usage_records"]
        list = [
            UsageRecord(
                RefId(record["id"]),
            )
            for record in self._transaction_db["usage_records"]
        ]

        return {record["id"]: record for record in list}

    @property
    def reservations(self) -> dict[RefId, Reservation]:
        return super().reservations

    def add_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        self._transaction_db.reload()
        return usage_record

    def finish_usage_record(self, usage_record: UsageRecord) -> UsageRecord:
        self._transaction_db.reload()
        return usage_record
