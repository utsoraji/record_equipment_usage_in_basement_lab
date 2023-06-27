import io
import logging
import time

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from .credential import get_credentials

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleDriveWrapper:
    def __init__(self):
        creds = get_credentials(SCOPES)
        if creds is None:
            raise ValueError("Error: 認証情報が見つかりませんでした。")
        self._service = build("drive", "v3", credentials=creds)

    def download_file_to_memory(self, file_id: str) -> io.BytesIO:
        buffer = io.BytesIO()
        self._download_file(file_id, buffer)
        return buffer

    def download_file_to_file(self, file_id: str, file_name: str) -> None:
        file_io = io.FileIO(file_name, mode="wb")
        self._download_file(file_id, file_io)

    def _download_file(
        self, file_id: str, buffer: io.BytesIO | io.FileIO, timeout: int = 10
    ) -> None:
        request = self._service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        timeout: WaitTimeout = WaitTimeout(timeout)
        timeout.start()
        while done is False:
            status, done = downloader.next_chunk()
            if timeout.is_timeout():
                logging.warning(f"Time out for downloading {file_id}.")
                break


class WaitTimeout:
    def __init__(self, seconds: int) -> None:
        self._seconds = seconds

    def start(self) -> None:
        self._start_time = time.time()

    def is_timeout(self) -> bool:
        return time.time() - self._start_time > self._seconds
