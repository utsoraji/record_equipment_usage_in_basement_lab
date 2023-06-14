import gspread


class WorksheetAsTable:
    def __init__(self, worksheet: gspread.Worksheet) -> None:
        self._worksheet = worksheet
        self.load()

    def load(self) -> None:
        raw = self._worksheet.get_all_values()
        header = raw[0]
        values = raw[1:]

        self._cached_data = [dict(zip(header, row)) for row in values]

    def __item__(self, item):
        return self._cached_data[item]


class SpreadsheetAsDataBase:
    def __init__(self, client: gspread.Client, key: str):
        self._key = key
        self._sheet = client.open_by_key(key)
        self._tables = {
            ws.title: WorksheetAsTable(ws) for ws in self._sheet.worksheets()
        }

    @property
    def table_keys(self) -> list[str]:
        return self._tables.keys()

    def __getitem__(self, key: str) -> gspread.Worksheet:
        return self._tables[key]

    def reload(self) -> None:
        for table in self._tables.values():
            table.load()
