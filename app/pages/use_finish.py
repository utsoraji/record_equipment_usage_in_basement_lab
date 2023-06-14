from datetime import datetime

import pandas as pd
import streamlit as st

import app.session as session
from app.const import PageId
from app.model.usage_record import UsageRecord
from app.pages.base import BasePage


class UseFinishPage(BasePage):
    def __init__(self) -> None:
        super().__init__(PageId.USE_FINISH, "Finish to Use")

    def render(self) -> None:
        st.title(self.title)

        target: UsageRecord = session.get_cxt().target_usage_record
        if target is None:
            st.error("No usage record selected")
            st.stop()

        equipment_string = ", ".join(eq.name for eq in target.equipments)
        st.write(f"{equipment_string}")
        st.write(f"Started at {target.starting}")
        st.write(f"Estimated end at {target.end_estimate}")

        self.render_finish(target)

    def render_finish(self, target: UsageRecord) -> None:
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
        )

        if finish:
            st.write(f"Finish time: {finishtime}")
            # TODO
