from abc import abstractmethod

from src.domain.observer.context import Context


class Subscriber:
    @abstractmethod
    def notify(self, context: Context) -> None:
        ...


class ConcreteSubscriber(Subscriber):
    def notify(self, context: Context) -> None:
        print(
            f"{self} - Received <{context.get_message()}> from {context.get_sender()}"
        )
