from datetime import datetime

import pandas as pd
import streamlit as st
import streamlit_toggle as tog

import app.session as session
from app.const import PageId
from app.datastore.protocol import NewUsageRecord, TransactionController
from app.model.equipment import Equipment
from app.pages.base import BasePage
from app.pages.components.select_eqipments_grid import eqipments_grid
from app.pages.components.show_record_summary import show_record_summary


def check_license(new_usage: NewUsageRecord) -> list[str]:
    unlicensed = [
        eq
        for eq in new_usage.equipments
        if eq.check_license and not [l for l in new_usage.user.licenses if l == eq.id]
    ]
    return [f"You are not licensed to use {eq.name}." for eq in unlicensed]


def check_current_usage(
    new_usage: NewUsageRecord, transaction_controller: TransactionController
) -> list[str]:
    in_use: set[Equipment] = set()
    for u in transaction_controller.usage_records.values():
        in_use = in_use.union(u.equipments)
    return [
        f" {eq.name} is in use already."
        for eq in in_use.intersection(new_usage.equipments)
    ]


def check_reservation(
    new_usage: NewUsageRecord, transaction_controller: TransactionController
) -> list[str]:
    ret: list[str] = []
    for res in transaction_controller.reservations.values():
        booking = set(res.equipments).intersection(new_usage.equipments)
        ret.extend(
            [
                f" {eq.name} is reserved from {res.starting} to {res.end} by {res.user.name}."
                for eq in booking
            ]
        )

    return ret


class UseStartPage(BasePage):
    def __init__(self) -> None:
        super().__init__(PageId.USE_START, "Start to Use")

    def render(self) -> None:
        st.title(self.title)

        selected_equipments = eqipments_grid(
            session.get_svcs().master_provider.equipments.values(),
            "use_start__selected_equipments",
        )

        starttime = pd.to_datetime(datetime.now()).round("min")

        if self.toggle("Specify start time"):
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

        note = None
        if self.toggle("Write note"):
            note = st.text_area("Note", label_visibility="collapsed")

        new_record: NewUsageRecord = NewUsageRecord(
            user=session.get_cxt().current_user,
            equipments=selected_equipments,
            starting=starttime,
            note=note,
        )
        st.divider()
        show_record_summary(new_record)

        warnings: list[str] = self.check_warnings(new_record)
        for w in warnings:
            st.warning(w)

        start = st.button(
            len(warnings) > 0 and "Start anyway" or "Start",
            disabled=len(selected_equipments) == 0,
        )

        if start:
            with st.spinner("Saving..."):
                reslut = session.get_svcs().transaction_controller.add_usage_record(
                    new_record
                )
            # TODO
            session.get_cxt().goto(PageId.START)
            st.experimental_rerun()

    def check_warnings(self, new_usage: NewUsageRecord) -> list[str]:
        warnings: list[str] = []
        warnings += check_license(new_usage)
        warnings += check_current_usage(
            new_usage, session.get_svcs().transaction_controller
        )
        warnings += check_reservation(
            new_usage, session.get_svcs().transaction_controller
        )
        return warnings
