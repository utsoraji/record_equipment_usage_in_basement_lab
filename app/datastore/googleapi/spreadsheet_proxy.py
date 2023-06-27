import datetime
from typing import Any, Iterable, Tuple

import gspread
import gspread.utils as gsutils

from app.datastore.protocol import RefId


class WorksheetProxy:
    def __init__(self, worksheet: gspread.Worksheet) -> None:
        self._ws = worksheet
        self.load()

    def load(self) -> None:
        """
        Loads data unformatted from target worksheeet into a cached data via gspread.\n
        Empty values are replaced with None.
        """
        raw = self._ws.get_values(
            value_render_option=gsutils.ValueRenderOption.unformatted
        )
        if len(raw) == 0:
            return

        self._header: list[str] = raw[0]
        values = raw[1:]
        for i in range(len(values)):
            for j in range(len(values[i])):
                if type(values[i][j]) == str:
                    values[i][j] = values[i][j].strip()
                    values[i][j] = None if values[i][j] == "" else values[i][j]

        self._cached_data = [dict(zip(self._header, row)) for row in values]

    def __len__(self) -> int:
        return len(self._cached_data)

    def append_row(self, data: dict[str, Any]) -> None:
        """
        Appends a row to the target worksheet.\n
        Values are added only if their key is in both of the header and data.keys().
        """
        row = [data.get(key) for key in self._header]
        self._ws.append_row(row)

    def find_rows(self, condition: dict[str, Any]) -> Tuple[int, dict[str, Any]]:
        def check_condition(row: dict[str, Any]) -> bool:
            for key, value in condition.items():
                if isinstance(value, RefId):
                    value = str(value)
                if row.get(key) != value:
                    return False
            return True

        return [(i, row) for i, row in self.with_index() if check_condition(row)]

    def delete_row(self, condition: dict[str, Any]) -> None:
        targets = self.find_rows(condition)
        if len(targets) == 0:
            return

        self._ws.delete_row(targets[0][0])

    def with_index(self) -> Iterable[Tuple[int, dict[str, Any]]]:
        return [(i + 2, data) for i, data in enumerate(self._cached_data)]

    def __iter__(self):
        return self._cached_data.__iter__()


class SpreadsheetProxy:
    def __init__(self, client: gspread.Client, key: str):
        self._key = key
        self._ss = client.open_by_key(key)
        self._wss = {ws.title: WorksheetProxy(ws) for ws in self._ss.worksheets()}
        self._last_loaded_at = datetime.datetime.now()

    @property
    def table_keys(self) -> list[str]:
        return self._wss.keys()

    def __getitem__(self, key: str) -> gspread.Worksheet:
        return self._wss[key]

    def reload(self) -> None:
        for table in self._wss.values():
            table.load()
        self._last_loaded_at = datetime.datetime.now()

    @property
    def last_loaded_at(self) -> datetime.datetime:
        return self._last_loaded_at
