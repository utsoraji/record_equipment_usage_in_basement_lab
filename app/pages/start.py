from typing import Any

import pandas as pd
import streamlit as st

import app.session as session
from app.const import PageId
from app.model.usage_record import UsageRecord
from app.pages.base import BasePage


class StartPage(BasePage):
    def __init__(self) -> None:
        super().__init__(PageId.START, "Start")

    def render(self) -> None:
        st.title(self.title)
        st.button("Start", on_click=lambda: session.get_cxt().goto(PageId.ENTRY))

        def usage_record_to_rowdata(record: UsageRecord) -> dict[str, Any]:
            return {
                "equipments": ", ".join(eq.name for eq in record.equipments),
                "user": record.user.name,
                "starting": record.starting,
                "end_estimate": record.end_estimate,
                "note": record.note,
            }

        st.write("List of Equipments in Use")
        df = pd.DataFrame(
            [
                usage_record_to_rowdata(r)
                for r in session.get_svcs().transaction_controller.usage_records.values()
            ]
        )
        st.table(df)
