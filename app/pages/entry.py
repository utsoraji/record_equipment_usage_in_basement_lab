import pandas as pd
import streamlit as st

from app.const import ContextKey, PageId
from app.model.user import User
from app.pages.base import BasePage
from app.session import StreamlitSessionCoodinator


class EntryPage(BasePage):
    def __init__(self, ssc: StreamlitSessionCoodinator) -> None:
        super().__init__(PageId.ENTRY, "Entry", ssc)

    def render(self) -> None:
        st.title(self.title)

        not_selected = User.empty()
        options: list[User] = [not_selected] + list(self.ssc.data_provider.users)
        selected = st.selectbox(
            "Select your name",
            options,
            format_func=lambda x: x.name,
        )

        if selected != not_selected:
            self.ssc.set_user(selected)

        st.button(
            "Start to Use Equipments",
            on_click=lambda: self.ssc.set_current_page(PageId.USE_START),
            disabled=selected == not_selected,
        )

        st.divider()

        usages = [u for u in self.ssc.data_provider.usage_records if u.user == selected]
        for i, u in enumerate(usages):

            def on_click_record():
                self.ssc.set_context(ContextKey.USAGE_RECORD, u)
                self.ssc.set_current_page(PageId.USE_FINISH)

            st.button(
                label=f"{u.equipment.name}",
                key=u.id,
                on_click=on_click_record,
            )
