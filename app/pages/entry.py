import streamlit as st

import app.session as session
from app.const import PageId
from app.model.user import User
from app.pages.base import BasePage


class EntryPage(BasePage):
    def __init__(self) -> None:
        super().__init__(PageId.ENTRY, "Entry")

    def render(self) -> None:
        st.title(self.title)

        not_selected = User.empty()
        options: list[User] = [not_selected] + list(
            session.get_svcs().master_provider.users.values()
        )
        selected = st.selectbox(
            "Select your name",
            options,
            format_func=lambda x: x.name,
        )

        if selected != not_selected:
            session.get_cxt().set_user(selected)

        st.button(
            "Start to Use Equipments",
            on_click=lambda: session.get_cxt().goto(PageId.USE_START),
            disabled=selected == not_selected,
        )

        st.divider()

        usages = [
            u
            for u in session.get_svcs().transaction_controller.usage_records.values()
            if u.user == selected
        ]
        for u in usages:

            def on_click_record():
                session.get_cxt().set_target_usage_record(u)
                session.get_cxt().goto(PageId.USE_FINISH)

            st.button(
                label=",".join(eq.name for eq in u.equipments),
                key=u.id,
                on_click=on_click_record,
            )
