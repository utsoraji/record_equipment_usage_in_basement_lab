from app.const import PageId
from app.model.usage_record import UsageRecord
from app.model.user import User


class AppContext:
    def __init__(self, initial_page: PageId):
        self._current_page: PageId = initial_page
        self._back_destination: PageId = None
        self._current_user: User = None
        self._target_usage_record: UsageRecord = None

    def goto(self, page_id: PageId, arrow_back=True) -> None:
        if page_id == self._current_page:
            return
        self._back_destination = self._current_page if arrow_back else None
        self._current_page = page_id

    def go_back(self) -> None:
        if self._back_destination is None:
            return
        self._current_page = self._back_destination

    def set_user(self, user: User) -> None:
        self._current_user = user

    def set_target_usage_record(self, usage_record: UsageRecord) -> None:
        self._target_usage_record = usage_record

    @property
    def current_page(self) -> PageId:
        return self._current_page

    @property
    def back_destination(self) -> PageId:
        return self._back_destination

    @property
    def previous_page(self) -> PageId:
        return self._back_destination

    @property
    def current_user(self) -> User:
        return self._current_user

    @property
    def target_usage_record(self) -> UsageRecord:
        return self._target_usage_record
