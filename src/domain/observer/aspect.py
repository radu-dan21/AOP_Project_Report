import functools

import aspectlib


@aspectlib.Aspect(bind=True)
def notify_subscribers_aspect(cutpoint, *args, **kwargs):
    """
    Aspect used for notifying subscribers after publisher changes
    If the Publisher method is decorated with the `changes_state` decorator, subscribers
    will get notified of changes
    :param cutpoint: Publisher (or Publisher subclass) method
    :param args: arguments for cutpoint
    :param kwargs: keyword arguments for cutpoint
    :return: return value of cutpoint
    """
    result = yield aspectlib.Proceed
    if getattr(cutpoint, "changes_state", None) is True:
        args[0].notify_subscribers(result[1])
        result = result[0]
    yield aspectlib.Return(result)


def changes_state(msg_format: str | None = None):
    """
    Decorator that should be used with methods that modify publisher state
    :param msg_format: message format used to send notifications to subscribers
        - this is automatically formatted with the decorated function's return value
    :return: decorated function
    """

    def inner(func):
        func.changes_state = True

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            msg = msg_format and msg_format.format(result)
            return result, msg

        return wrapper

    return inner
