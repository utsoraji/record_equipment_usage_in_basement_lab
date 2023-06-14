from abc import ABC, abstractmethod

from app.const import PageId


class BasePage(ABC):
    def __init__(self, page_id: PageId, title: str) -> None:
        self.page_id = page_id
        self.title = title

    @abstractmethod
    def render(self) -> None:
        pass
