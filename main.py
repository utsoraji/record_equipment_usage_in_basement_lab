import streamlit as st

from app.app import App
from app.datastore.mock import MockDataManipulator, MockDataProvider
from app.pages.entry import EntryPage
from app.pages.start import StartPage
from app.pages.use_finish import UseFinishPage
from app.pages.use_start import UseStartPage
from app.session import StreamlitSessionCoodinator


def init_app(ssc: StreamlitSessionCoodinator):
    pages = [
        StartPage(ssc),
        EntryPage(ssc),
        UseStartPage(ssc),
        UseFinishPage(ssc),
    ]

    return App(ssc, pages)


def init_session() -> StreamlitSessionCoodinator:
    ssc = StreamlitSessionCoodinator(
        data_provider=MockDataProvider(), data_manipulator=MockDataManipulator()
    )
    return ssc


def main():
    if not st.session_state.get("is_open", False):
        ssc = init_session()
        app = init_app(ssc)
        st.session_state.is_open = True
        st.session_state.app = app

    app = st.session_state.app

    app.render()


if __name__ == "__main__":
    main()
