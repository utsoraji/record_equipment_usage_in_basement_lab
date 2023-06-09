from datetime import date, datetime, time, timedelta

import pandas as pd
import streamlit as st

from app.const import PageId
from app.model.equipment import Equipment
from app.pages.base import BasePage
from app.session import StreamlitSessionCoodinator


class UseStartPage(BasePage):
    def __init__(self, ssc: StreamlitSessionCoodinator) -> None:
        super().__init__(PageId.USE_START, "Start to Use", ssc)

    def render(self) -> None:
        st.title(self.title)

        equipments: list[Equipment] = st.multiselect(
            "Select facilities",
            self.ssc.data_provider.equipments,
            format_func=lambda x: x.name,
        )

        starttime = pd.to_datetime(datetime.now()).round("min")

        if st.checkbox("Specify start time", value=False):
            d = st.date_input(
                "Start date",
                value=datetime.date(starttime),
                label_visibility="collapsed",
            )
            t = st.time_input(
                "Start time",
                value=datetime.time(starttime),
                label_visibility="collapsed",
            )

            starttime = datetime.combine(d, t)

        endtime = starttime
        with st.container():
            period = st.select_slider(
                "Period",
                [
                    "15 min",
                    "30 min",
                    "45 min",
                    "1 hour",
                    "2 hours",
                    "3 hours",
                    "4 hours",
                    "5 hours",
                    "6 hours",
                    "7 hours",
                    "8 hours",
                    "all day",
                    "later date",
                ],
            )
            if period == "15 min":
                endtime = starttime + timedelta(minutes=15)
            elif period == "30 min":
                endtime = starttime + timedelta(minutes=30)
            elif period == "45 min":
                endtime = starttime + timedelta(minutes=30)
            elif period == "1 hour":
                endtime = starttime + timedelta(hours=1)
            elif period == "2 hours":
                endtime = starttime + timedelta(hours=2)
            elif period == "3 hours":
                endtime = starttime + timedelta(hours=3)
            elif period == "4 hours":
                endtime = starttime + timedelta(hours=4)
            elif period == "5 hours":
                endtime = starttime + timedelta(hours=5)
            elif period == "6 hours":
                endtime = starttime + timedelta(hours=6)
            elif period == "7 hours":
                endtime = starttime + timedelta(hours=7)
            elif period == "8 hours":
                endtime = starttime + timedelta(hours=8)
            elif period == "all day":
                endtime = datetime.combine(date.today() + timedelta(days=1), time(0, 0))
            elif period == "later date":
                tomorrow = datetime.today() + timedelta(days=1)
                d = st.date_input(
                    "End date",
                    label_visibility="collapsed",
                    value=tomorrow,
                    min_value=tomorrow,
                )
                endtime = datetime.combine(d, time(23, 59))
            else:
                raise ValueError(f"Unknown period: {period}")

            st.write(f"Starting time: {starttime}")
            st.write(f"End time: {endtime}")

        any_warning_exists = False

        def check_license() -> bool:
            licensed = self.ssc.user.licenses
            unlicensed = [
                eq
                for eq in equipments
                if eq.check_license and not [l for l in licensed if l == eq.id]
            ]
            for eq in unlicensed:
                st.warning(f"You are not licensed to use {eq.name}.")
            return len(unlicensed) > 0

        any_warning_exists = check_license()

        start = st.button(
            any_warning_exists and "Start anyway" or "Start",
            disabled=len(equipments) == 0,
        )

        if start:
            st.write(f"Start time: {starttime}")
            # TODO
