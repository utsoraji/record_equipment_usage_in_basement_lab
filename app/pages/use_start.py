from datetime import datetime

import pandas as pd
import streamlit as st

import app.session as session
from app.const import PageId
from app.datastore.protocol import MasterProvider, NewUsageRecord, TransactionController
from app.model.equipment import Equipment
from app.pages.base import BasePage
from app.pages.components.select_eqipments_grid import eqipments_grid


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
    reserved: set[Equipment] = set()
    for res in transaction_controller.reservations.values():
        res = reserved.union(res.equipments)

    return [
        f" {eq.name} is reserved today."
        for eq in (reserved.intersection(new_usage.equipments))
    ]


class UseStartPage(BasePage):
    def __init__(self) -> None:
        super().__init__(PageId.USE_START, "Start to Use")

    def render(self) -> None:
        st.title(self.title)

        selected_equipments = eqipments_grid(
            session.get_svcs().master_provider.equipments.values(),
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

        st.divider()
        selected_names = ", ".join(eq.name for eq in selected_equipments)
        st.text(f"Selected:{selected_names}")
        st.text(f"Start at:{starttime}")

        any_warning_exists = False

        new_record: NewUsageRecord = NewUsageRecord(
            starting=starttime,
            end_estimate=None,
            equipments=selected_equipments,
            user=session.get_cxt().current_user,
        )

        warnings: list[str] = []
        warnings += check_license(new_record)
        warnings += check_current_usage(
            new_record, session.get_svcs().transaction_controller
        )
        warnings += check_reservation(
            new_record, session.get_svcs().transaction_controller
        )

        any_warning_exists = len(warnings) > 0
        for w in warnings:
            st.warning(w)

        start = st.button(
            any_warning_exists and "Start anyway" or "Start",
            disabled=len(selected_equipments) == 0,
        )

        if start:
            with st.spinner("Saving..."):
                reslut = session.get_svcs().transaction_controller.add_usage_record(
                    new_record
                )
                session.get_cxt().set_target_usage_record(reslut)
                session.get_cxt().goto(PageId.ENTRY)
            # TODO
