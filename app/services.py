from app.datastore.protocol import (
    MasterProvider,
    StaticResourceProvider,
    TransactionController,
)


class AppServiceContainer:
    def __init__(
        self,
        master_provider: MasterProvider,
        transaction_controller: TransactionController,
        static_resource_provider: StaticResourceProvider,
    ):
        self._master_provider = master_provider
        self._transaction_controller = transaction_controller
        self._static_resource_provider = static_resource_provider

    @property
    def master_provider(self) -> MasterProvider:
        return self._master_provider

    @property
    def transaction_controller(self) -> TransactionController:
        return self._transaction_controller

    @property
    def static_resource_provider(self) -> StaticResourceProvider:
        return self._static_resource_provider
