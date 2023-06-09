from datetime import date, datetime, time, timedelta

import pandas as pd
import streamlit as st

from app.const import ContextKey, PageId
from app.model.usage_record import UsageRecord
from app.pages.base import BasePage
from app.session import StreamlitSessionCoodinator


class UseFinishPage(BasePage):
    def __init__(self, ssc: StreamlitSessionCoodinator) -> None:
        super().__init__(
            PageId.USE_FINISH, "Finish to Use or Change Estimate Time", ssc
        )

    def render(self) -> None:
        st.title(self.title)

        usage_record: UsageRecord = self.ssc.read_context(ContextKey.USAGE_RECORD)
        if usage_record is None:
            st.error("No usage record selected")
            st.stop()

        st.write(f"{usage_record.equipment.name}")
        st.write(f"Started at {usage_record.starting}")
        st.write(f"Estimated end at {usage_record.end_estimate}")

        finish_tab, change_tab = st.tabs(["Finish to Use", "Change Estimate Time"])

        with finish_tab:
            self.render_finish(usage_record)

        with change_tab:
            self.render_change(usage_record)

    def render_finish(self, usage_record: UsageRecord) -> None:
        st.subheader("Finish to Use")
        finishtime = pd.to_datetime(datetime.now()).round("min")

        if st.checkbox("Specify finish time", value=False):
            d = st.date_input(
                "End date",
                value=datetime.date(finishtime),
                label_visibility="collapsed",
            )
            t = st.time_input(
                "End time",
                value=datetime.time(finishtime),
                label_visibility="collapsed",
            )

            finishtime = datetime.combine(d, t)

        finish = st.button(
            "Finish to Use",
            on_click=lambda: self.ssc.set_current_page(PageId.USE_START),
        )

        if finish:
            st.write(f"Finish time: {finishtime}")
            # TODO

    def render_change(self, usage_record: UsageRecord) -> None:
        st.subheader("Change Estimate Time")
        estimatetime = usage_record.end_estimate

        d = st.date_input(
            "Estimate date",
            value=datetime.date(estimatetime),
            label_visibility="collapsed",
        )
        t = st.time_input(
            "Estimate time",
            value=datetime.time(estimatetime),
            label_visibility="collapsed",
        )

        estimatetime = datetime.combine(d, t)

        finish = st.button(
            "Change estimate end time",
            on_click=lambda: self.ssc.set_current_page(PageId.USE_START),
        )

        if finish:
            st.write(f"Finish time: {estimatetime}")
            # TODO
