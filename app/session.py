import streamlit as st

from app.app import App
from app.const import PageId, SessionKey
from app.context import AppContext
from app.datastore.protocol import MasterProvider, TransactionController
from app.services import AppServiceContainer


def init_session(
    app: App,
    initial_page: PageId,
    master_provider: MasterProvider,
    transaction_controller: TransactionController,
) -> None:
    st.session_state[SessionKey.APP] = app
    st.session_state[SessionKey.CONTEXT] = AppContext(initial_page)
    st.session_state[SessionKey.SERVICES] = AppServiceContainer(
        master_provider, transaction_controller
    )
    st.session_state[SessionKey.IS_INITIALIZED] = True


def is_initialized() -> bool:
    return st.session_state.get(SessionKey.IS_INITIALIZED, False)


def reset():
    st.session_state[SessionKey.IS_INITIALIZED] = False


def get_app() -> App:
    return st.session_state[SessionKey.APP]


def get_cxt() -> AppContext:
    return st.session_state[SessionKey.CONTEXT]


def get_svcs() -> AppServiceContainer:
    return st.session_state[SessionKey.SERVICES]
