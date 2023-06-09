from abc import ABC, abstractmethod

from app.const import PageId
from app.session import StreamlitSessionCoodinator


class BasePage(ABC):
    def __init__(
        self, page_id: PageId, title: str, ssc: StreamlitSessionCoodinator
    ) -> None:
        self.page_id = page_id
        self.title = title
        self.ssc = ssc

    @abstractmethod
    def render(self) -> None:
        pass
