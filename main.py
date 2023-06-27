import app.session as session
from app.app import App
from app.const import PageId
from app.datastore.googleapi.g_master_provider import GoogleMasterProvider
from app.datastore.googleapi.g_static_resource_provider import (
    GoogleStaticResourceProvider,
)
from app.datastore.googleapi.g_transaction_contoroller import (
    GoogleTransactionController,
)

# from app.datastore.mock.mock import MockMasterProvider, MockTransactionController
from app.pages.entry import EntryPage
from app.pages.start import StartPage
from app.pages.use_finish import UseFinishPage
from app.pages.use_start import UseStartPage


def init_app():
    return App(
        [
            StartPage(),
            EntryPage(),
            UseStartPage(),
            UseFinishPage(),
        ]
    )


def st_loop():
    """
    Run by Streamlit every time when state is changed.\n
    Use session state to store app itself and other states to show appropriate pages depending on operation by user.

    Parameters:
    None

    Returns:
    None
    """
    if not session.is_initialized():
        master_provider = GoogleMasterProvider()
        transaction_controller = GoogleTransactionController(master_provider)
        static_resource_provider = GoogleStaticResourceProvider()
        session.init_session(
            init_app(),
            PageId.START,
            master_provider,
            transaction_controller,
            static_resource_provider,
        )
        # init_app(), PageId.START, GoogleDataProvider(), MockDataManipulator()

    if session.to_be_restart():
        # To avoid accessing google api per restart, distinguish initialize and restart.
        session.restart_session(
            init_app(),
            PageId.START,
        )

    session.get_app().render()


if __name__ == "__main__":
    st_loop()
