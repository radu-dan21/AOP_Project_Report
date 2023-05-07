import aspectlib

from src.domain.aspect.logging import logging_aspect
from src.domain.aspect.performance import performance_aspect
from src.domain.models.base import BaseModel
from src.domain.observer.aspect import notify_subscribers_aspect
from src.domain.observer.publisher import Publisher


def weave():
    aspectlib.weave(Publisher, notify_subscribers_aspect, subclasses=True)
    aspectlib.weave(BaseModel, [logging_aspect, performance_aspect], subclasses=True)
