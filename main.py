import app.session as session
from app.app import App
from app.const import PageId
from app.datastore.mock.mock import MockDataManipulator, MockDataProvider
from app.pages.entry import EntryPage
from app.pages.start import StartPage
from app.pages.use_finish import UseFinishPage
from app.pages.use_start import UseStartPage


def init_session():
    session.init_session(PageId.START, MockDataProvider(), MockDataManipulator())


def init_app():
    return App(
        [
            StartPage(),
            EntryPage(),
            UseStartPage(),
            UseFinishPage(),
        ]
    )


def main():
    if not session.is_initialized():
        session.init_session(
            init_app(), PageId.START, MockDataProvider(), MockDataManipulator()
        )

    session.get_app().render()


if __name__ == "__main__":
    main()
