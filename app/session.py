from typing import Any

import streamlit as st

from app.const import ContextKey, PageId, SessionKey
from app.datastore.protocol import DataManipulator, DataProvider
from app.model.user import User


class StreamlitSessionCoodinator:
    def __init__(
        self, data_provider: DataProvider, data_manipulator: DataManipulator
    ) -> None:
        self._session_state = st.session_state
        self._session_state[SessionKey.CURRENT_PAGE] = PageId.START
        self._session_state[SessionKey.CURRENT_USER] = None
        self._session_state[SessionKey.DATA_PROVIDER] = data_provider
        self._session_state[SessionKey.DATA_MANIPULATOR] = data_manipulator
        self._session_state[SessionKey.CONTEXT] = dict()

    @property
    def current_page(self) -> PageId:
        return self._session_state[SessionKey.CURRENT_PAGE]

    def set_current_page(self, page_id: PageId) -> None:
        self._session_state[SessionKey.CURRENT_PAGE] = page_id

    @property
    def user(self) -> User:
        return self._session_state[SessionKey.CURRENT_USER]

    def set_user(self, user: User) -> None:
        self._session_state[SessionKey.CURRENT_USER] = user

    @property
    def data_provider(self) -> DataProvider:
        return self._session_state[SessionKey.DATA_PROVIDER]

    def read_context(self, key: ContextKey) -> Any:
        if(key not in self._session_state[SessionKey.CONTEXT].keys()):
            return None
        return self._session_state[SessionKey.CONTEXT][key]

    def set_context(self, key: ContextKey, value: Any) -> None:
        self._session_state[SessionKey.CONTEXT][key] = value
