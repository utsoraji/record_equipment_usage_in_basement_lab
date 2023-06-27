import hashlib

import streamlit as st
from streamlit_pills import pills

import app.session as session
from app.const import PageId
from app.model.labo import Labo
from app.model.user import User, UserRole
from app.pages.base import BasePage

EMPTY_USER: User = User(
    "__empty__",
    "-",
    "-",
    "-",
)


LABO_ALL: Labo = Labo(
    "__all__",
    "All",
    "すべて",
)


class EntryPage(BasePage):
    def __init__(self) -> None:
        super().__init__(PageId.ENTRY, "Entry")

    def render(self) -> None:
        st.title(self.title)

        selected = user_selector()

        if selected != EMPTY_USER:
            session.get_cxt().set_user(selected)

        st.button(
            "Start to Use Equipments",
            on_click=lambda: session.get_cxt().goto(PageId.USE_START),
            disabled=selected == EMPTY_USER,
        )

        st.divider()
        print(len(session.get_svcs().transaction_controller.usage_records.values()))
        usages = [
            u
            for u in session.get_svcs().transaction_controller.usage_records.values()
            if selected.role == UserRole.ADMIN or u.user == selected
        ]
        print(selected.role == UserRole.ADMIN)
        print(selected.role.value)
        print(UserRole.ADMIN.value)
        for u in usages:

            def on_click_record():
                session.get_cxt().set_target_usage_record(u)
                session.get_cxt().goto(PageId.USE_FINISH)

            st.button(
                label=",".join(eq.name for eq in u.equipments),
                key=u.id,
                on_click=on_click_record,
            )


def user_selector() -> User:
    master = session.get_svcs().master_provider
    labo = pills(
        label="Select laboratory",
        options=[LABO_ALL] + list(master.labos.values()),
        format_func=lambda x: x.name,
    )

    user_options = (
        [EMPTY_USER] + list(master.users.values())
        if labo == LABO_ALL
        else [EMPTY_USER] + [u for u in master.users.values() if u.labo == labo]
    )

    return st.selectbox(
        "Select your name",
        user_options,
        format_func=lambda x: x.name,
    )
