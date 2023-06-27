from abc import ABC, abstractmethod

import streamlit_toggle as tog

from app.const import PageId


class BasePage(ABC):
    def __init__(self, page_id: PageId, title: str) -> None:
        self.page_id = page_id
        self.title = title

    def toggle(self, label: str) -> bool:
        return tog.st_toggle_switch(
            label=label,
            default_value=False,
            label_after=True,
        )

    @abstractmethod
    def render(self) -> None:
        pass
