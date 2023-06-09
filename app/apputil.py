import streamlit as st

from app.const import ContextKey, PageId
from app.session import StreamlitSessionCoodinator


def back_destination(ssc: StreamlitSessionCoodinator) -> PageId:
    current = ssc.current_page
    dest = ssc.read_context(ContextKey.BACK_DESTINATION)
    if dest != current:
        return dest
    return None


def goto(ssc: StreamlitSessionCoodinator, page_id: PageId, arrow_back=True):
    ssc.set_context(
        ContextKey.BACK_DESTINATION, ssc.current_page if arrow_back else None
    )

    ssc.set_current_page(page_id)


def reset():
    st.session_state.is_open = False
