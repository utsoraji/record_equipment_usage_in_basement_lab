import gspread
import gspread.utils as gsutils


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
        self._header = raw[0]
        values = raw[1:]
        for i in range(len(values)):
            for j in range(len(values[i])):
                if type(values[i][j]) == str:
                    values[i][j] = values[i][j].strip()
                    values[i][j] = None if values[i][j] == "" else values[i][j]

        self._cached_data = [dict(zip(self._header, row)) for row in values]

    def append_row(self, data: dict[str, str]) -> None:
        """
        Appends a row to the target worksheet.
        Values are added only if their key is in the header.
        """
        row = [data[key] for key in self._header]
        self._ws.append_row(row)

    def __iter__(self):
        return self._cached_data.__iter__()


class SpreadsheetProxy:
    def __init__(self, client: gspread.Client, key: str):
        self._key = key
        self._ss = client.open_by_key(key)
        self._wss = {ws.title: WorksheetProxy(ws) for ws in self._ss.worksheets()}

    @property
    def table_keys(self) -> list[str]:
        return self._wss.keys()

    def __getitem__(self, key: str) -> gspread.Worksheet:
        return self._wss[key]

    def reload(self) -> None:
        for table in self._wss.values():
            table.load()
