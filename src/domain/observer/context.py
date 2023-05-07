from abc import abstractmethod


class Context:
    @abstractmethod
    def get_sender(self) -> str:
        ...

    @abstractmethod
    def get_message(self) -> str | None:
        ...


class ConcreteContext(Context):
    def __init__(self, sender: str, message: str | None):
        self._sender: str = sender
        self._message: str | None = message

    def get_sender(self) -> str:
        return self._sender

    def get_message(self) -> str | None:
        return self._message
