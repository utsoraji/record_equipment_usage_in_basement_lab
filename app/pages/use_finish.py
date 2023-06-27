from datetime import datetime

import pandas as pd
import streamlit as st

import app.session as session
from app.const import PageId
from app.model.usage_record import UsageRecord
from app.pages.base import BasePage
from app.pages.components.show_record_summary import show_record_summary


class UseFinishPage(BasePage):
    def __init__(self) -> None:
        super().__init__(PageId.USE_FINISH, "Finish to Use")

    def render(self) -> None:
        st.title(self.title)

        target: UsageRecord = session.get_cxt().target_usage_record
        if target is None:
            st.error("No usage record selected")
            st.sidebar.button("Restart", on_click=session.restart)
            st.stop()

        show_record_summary(target)

        st.divider()

        finishtime = pd.to_datetime(datetime.now()).round("min")

        if self.toggle("Specify finish time"):
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

        if self.toggle("Write note"):
            note = st.text_area("Note", value=target.note, label_visibility="collapsed")

        st.divider()

        finish = st.button(
            "Finish to Use",
        )

        if finish:
            with st.spinner("Saving..."):
                result = session.get_svcs().transaction_controller.finish_usage_record(
                    UsageRecord(
                        id=target.id,
                        user=target.user,
                        equipments=target.equipments,
                        starting=target.starting,
                        end_estimate=target.end_estimate,
                        end_actual=finishtime,
                        note=note,
                    )
                )
            session.get_cxt().goto(PageId.START)
            st.experimental_rerun()
