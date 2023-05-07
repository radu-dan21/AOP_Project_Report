from abc import abstractmethod

from src.domain.observer.context import ConcreteContext, Context
from src.domain.observer.subscriber import Subscriber


class Publisher:
    @abstractmethod
    def get_subscribers(self) -> list[Subscriber]:
        ...

    @abstractmethod
    def subscribe(self, subscriber: Subscriber) -> None:
        ...

    @abstractmethod
    def unsubscribe(self, subscriber: Subscriber) -> None:
        ...

    def get_context(self, message: str | None = None) -> Context:
        return ConcreteContext(str(self), message)

    def notify_subscribers(self, message: str | None = None) -> None:
        context: Context = self.get_context(message)
        for s in self.get_subscribers():
            s.update(context)
