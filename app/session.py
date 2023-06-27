import streamlit as st

from app.app import App
from app.const import PageId, SessionKey
from app.context import AppContext
from app.datastore.protocol import (
    MasterProvider,
    StaticResourceProvider,
    TransactionController,
)
from app.services import AppServiceContainer


def init_session(
    app: App,
    initial_page: PageId,
    master_provider: MasterProvider,
    transaction_controller: TransactionController,
    static_resource_provider: StaticResourceProvider,
) -> None:
    st.session_state.clear()
    st.session_state[SessionKey.APP] = app
    st.session_state[SessionKey.CONTEXT] = AppContext(initial_page)
    st.session_state[SessionKey.SERVICES] = AppServiceContainer(
        master_provider, transaction_controller, static_resource_provider
    )
    st.session_state[SessionKey.IS_INITIALIZED] = True
    st.session_state[SessionKey.TO_BE_RESTART] = False


def restart_session(
    app: App,
    initial_page: PageId,
) -> None:
    services = st.session_state[SessionKey.SERVICES]
    st.session_state.clear()
    st.session_state[SessionKey.APP] = app
    st.session_state[SessionKey.CONTEXT] = AppContext(initial_page)
    st.session_state[SessionKey.SERVICES] = services
    st.session_state[SessionKey.IS_INITIALIZED] = True
    st.session_state[SessionKey.TO_BE_RESTART] = False


def is_initialized() -> bool:
    return st.session_state.get(SessionKey.IS_INITIALIZED, False)


def reset():
    st.session_state[SessionKey.IS_INITIALIZED] = False


def to_be_restart() -> bool:
    return st.session_state.get(SessionKey.TO_BE_RESTART, False)


def restart():
    st.session_state[SessionKey.TO_BE_RESTART] = True


def get_app() -> App:
    return st.session_state[SessionKey.APP]


def get_cxt() -> AppContext:
    return st.session_state[SessionKey.CONTEXT]


def get_svcs() -> AppServiceContainer:
    return st.session_state[SessionKey.SERVICES]
