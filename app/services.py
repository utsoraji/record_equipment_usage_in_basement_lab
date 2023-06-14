from app.datastore.protocol import MasterProvider, TransactionController


class AppServiceContainer:
    def __init__(
        self,
        master_provider: MasterProvider,
        transaction_controller: TransactionController,
    ):
        self._master_provider = master_provider
        self._transaction_controller = transaction_controller

    @property
    def master_provider(self) -> MasterProvider:
        return self._master_provider

    @property
    def transaction_controller(self) -> TransactionController:
        return self._transaction_controller
