from src.domain.models.base import BaseModel
from src.domain.observer import ConcreteSubscriber


class User(ConcreteSubscriber, BaseModel):
    ...
