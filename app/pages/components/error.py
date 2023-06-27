import streamlit as st

import app.session as session


def show_error(msg: str) -> None:
    st.error(msg)
    st.sidebar.button("Restart", on_click=session.restart)
    st.stop()
