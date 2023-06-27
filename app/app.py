import streamlit as st

import app.session as session
from app.pages.base import BasePage


class App:
    def __init__(self, pages: list[BasePage]):
        self.pages = {page.page_id: page for page in pages}
        # TODO remove print
        print(self.pages.keys())

    def render(self):
        st.sidebar.button("Reset", on_click=session.reset)
        st.sidebar.button("Restart", on_click=session.restart)
        st.sidebar.button(
            "Back",
            on_click=lambda: session.get_cxt().go_back(),
            disabled=session.get_cxt().back_destination is None,
        )
        # TODO remove print
        print(session.get_cxt().current_page)
        self.pages[session.get_cxt().current_page].render()
        pass
