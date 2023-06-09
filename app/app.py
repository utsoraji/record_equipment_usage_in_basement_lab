import streamlit as st

import app.apputil as util
from app.pages.base import BasePage
from app.session import StreamlitSessionCoodinator


class App:
    def __init__(self, ssc: StreamlitSessionCoodinator, pages: list[BasePage]):
        self.ssc = ssc
        self.pages = {page.page_id: page for page in pages}
        # TODO remove print
        print(self.pages.keys())

    def render(self):
        st.sidebar.button("Reset", on_click=util.reset)
        back_destination = util.back_destination(self.ssc)
        st.sidebar.button(
            "Back",
            on_click=lambda: util.goto(self.ssc, back_destination, arrow_back=False),
            disabled=back_destination is None,
        )
        # TODO remove print
        print(self.ssc.current_page)
        self.pages[self.ssc.current_page].render()
        pass
