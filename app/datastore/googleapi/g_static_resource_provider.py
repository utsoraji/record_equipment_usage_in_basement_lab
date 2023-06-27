import io
import os

import streamlit as st

from app.datastore.protocol import StaticResourceProvider

from .drive_service import GoogleDriveWrapper

CACHE_DIR = "cache"


class GoogleStaticResourceProvider(StaticResourceProvider):
    def __init__(self):
        self._drive_client = GoogleDriveWrapper()

    @st.cache_resource(show_spinner="Loading...")
    def get_image(_self, id: str) -> io.BytesIO:
        cache_path = os.path.join(CACHE_DIR, id)
        if not os.path.exists(cache_path):
            _self.download_image(id)

        with open(cache_path, "rb") as fh:
            return io.BytesIO(fh.read())

    def download_image(self, id: str) -> None:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        cache_path = os.path.join(CACHE_DIR, id)
        if not os.path.exists(cache_path):
            self._drive_client.download_file_to_file(id, cache_path)
