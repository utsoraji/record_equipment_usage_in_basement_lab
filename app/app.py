import streamlit as st
from app.pages.base import BasePage
from app.session import StreamlitSessionCoodinator


class App:
    def __init__(self, ssc: StreamlitSessionCoodinator, pages: list[BasePage]):
        self.ssc = ssc
        self.pages = {page.page_id: page for page in pages}
        print(self.pages.keys())

    def render(self):
        def reset():
            st.session_state.is_open = False

        st.sidebar.button("Reset", on_click=reset)
        print(self.ssc.current_page)
        self.pages[self.ssc.current_page].render()
        pass
