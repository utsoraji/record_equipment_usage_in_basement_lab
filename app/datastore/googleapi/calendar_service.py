import datetime

import pandas as pd
from googleapiclient.discovery import build


class GoogleCalendarService:
    def __init__(self, credentials, calendar_id="primary"):
        self._service = build("calendar", "v3", credentials=credentials)
        self._calendar_id = calendar_id

    def get_events(self, time_min=None, time_max=None):
        if time_min is None:
            time_min = pd.to_datetime(datetime.datetime().utcnow()).round("D")
        if time_max is None:
            time_max = time_min + datetime.timedelta(days=1)

        def format_time(datetime: datetime.datetime) -> str:
            return datetime.isoformat() + ("Z" if datetime.tzinfo is None else "")

        events_result = (
            self._service.events()
            .list(
                calendarId=self._calendar_id,
                timeMin=format_time(time_min),
                timeMax=format_time(time_max),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        return events
