import functools

from abc import abstractmethod

from src.domain import ValidationError


class MenuEndException(Exception):
    ...


def catch_validation_exception(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            print(e)

    return inner


class AbstractMenu:
    @classmethod
    @abstractmethod
    def _get_menu_options(cls) -> list[tuple[str, callable]]:
        ...

    @staticmethod
    def _input_string(prompt: str) -> str:
        value = input(prompt).strip()
        if not value:
            raise ValidationError("Input can't be empty!")
        return value

    @staticmethod
    def _input_int(
        prompt: str,
        exclusive_bounds: tuple[int | None, int | None] = (None, None),
    ) -> int:
        try:
            value = int(input(prompt))
        except ValueError:
            raise ValidationError("Input must be an integer!")

        lb, ub = exclusive_bounds
        if (lb is not None and value <= lb) or (ub is not None and value >= ub):
            raise ValidationError(f"Input must be an integer between ({lb}, {ub})")

        return value

    @classmethod
    def __input_option(cls, option_count: int) -> int | None:
        try:
            return cls._input_int("Input your option: ", (-1, option_count))
        except ValidationError:
            return None

    @staticmethod
    def __exit_callable():
        raise MenuEndException

    @classmethod
    def run(cls):
        menu_options: list[tuple[str, callable]] = cls._get_menu_options()
        menu_options.insert(0, ("Exit", cls.__exit_callable))
        try:
            while True:
                print()
                for idx, (option_text, _option_callable) in enumerate(menu_options):
                    print(f"{idx}. {option_text}")
                option = cls.__input_option(len(menu_options))
                if option is None:
                    print("\nInvalid option!")
                else:
                    menu_options[option][1]()
        except MenuEndException:
            pass
