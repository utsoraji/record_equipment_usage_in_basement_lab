import pandas as pd
import streamlit as st

import app.apputil as util
from app.const import PageId
from app.pages.base import BasePage
from app.session import StreamlitSessionCoodinator


class StartPage(BasePage):
    def __init__(self, ssc: StreamlitSessionCoodinator) -> None:
        super().__init__(PageId.START, "Start", ssc)

    def render(self) -> None:
        st.title(self.title)
        st.button("Start", on_click=lambda: util.goto(self.ssc, PageId.ENTRY))

        def convert_usage_record(UsageRecord):
            return {
                "equipment": UsageRecord.equipment.name,
                "user": UsageRecord.user.name,
                "starting": UsageRecord.starting,
                "end_estimate": UsageRecord.end_estimate,
                "note": UsageRecord.note,
            }

        df = pd.DataFrame(
            [convert_usage_record(r) for r in self.ssc.data_provider.usage_records]
        )
        st.table(df)
