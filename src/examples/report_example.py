import logging
import sys

import aspectlib


# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# redirect logger output to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


@aspectlib.Aspect(bind=True)
def log(cutpoint, *args, **kwargs):
    result = yield aspectlib.Proceed(*args, **kwargs)
    function_name: str = cutpoint.__name__
    logger.info(
        f"\nCalled `{function_name}`"
        f"\nArgs: {args}"
        f"\nKwargs: {kwargs}"
        f"\nResult: {result}"
        f"\n"
    )
    yield aspectlib.Return(result)


class Calculator:
    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b

    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b


def do_math(a, b):
    print(f"a = {a}; b = {b}")
    print(f"a + b = {a} + {b} = {Calculator.add(a, b)}")
    print(f"a * b = {a} * {b} = {Calculator.multiply(a, b)}")


if __name__ == "__main__":
    r: aspectlib.Rollback = aspectlib.weave(Calculator, log)
    print("\nShould be logged:")
    do_math(3, 5)

    r.rollback()
    print("\nShould NOT be logged:")
    do_math(7, 1)
