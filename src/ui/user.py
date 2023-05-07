from peewee import DoesNotExist
from src.domain import ValidationError
from src.service import Service
from src.ui.base import AbstractMenu, catch_validation_exception
from src.ui.common import get_weather_stations_and_subscribed_users


class UserMenu(AbstractMenu):
    @classmethod
    def _get_menu_options(cls) -> list[tuple[str, callable]]:
        return [
            ("Add user", cls._add_user),
            ("Get users", cls._get_users),
            ("Change user name", cls._update_user),
            ("Remove user", cls._delete_user),
            ("Get subscriptions", get_weather_stations_and_subscribed_users),
            ("Subscribe user", cls._subscribe_user),
            ("Unsubscribe user", cls._unsubscribe_user),
        ]

    @classmethod
    @catch_validation_exception
    def _add_user(cls):
        cls._get_users()
        name = cls._input_string("\nPlease enter user name: ")
        Service.add_user(name)
        print("User added successfully")

    @staticmethod
    def _get_users():
        users = Service.get_users()
        if not users:
            print("\nThere are no users!")
        else:
            print("\nUsers:")
        for u in users:
            print(u)

    @classmethod
    @catch_validation_exception
    def _update_user(cls):
        cls._get_users()
        user_id = cls._input_int("Please enter user id: ", (0, None))
        name = cls._input_string("Please enter user name: ")
        try:
            Service.update_user(user_id, name)
        except DoesNotExist:
            raise ValidationError("User does not exist!")
        print("User updated successfully")

    @classmethod
    @catch_validation_exception
    def _delete_user(cls):
        cls._get_users()
        user_id = cls._input_int("Please enter user id: ", (0, None))
        Service.delete_user(user_id)
        print("User deleted successfully")

    @classmethod
    @catch_validation_exception
    def _subscribe_user(cls):
        get_weather_stations_and_subscribed_users()
        cls._get_users()
        station_id = cls._input_int("\nPlease enter station id: ", (0, None))
        user_id = cls._input_int("Please enter user id: ", (0, None))
        try:
            Service.subscribe_user_to_weather_station(user_id, station_id)
        except DoesNotExist:
            raise ValidationError("Invalid user and/or weather station id!")
        print("User subscribed successfully")

    @classmethod
    @catch_validation_exception
    def _unsubscribe_user(cls):
        get_weather_stations_and_subscribed_users()
        station_id = cls._input_int("\nPlease enter station id: ", (0, None))
        user_id = cls._input_int("Please enter user id: ", (0, None))
        try:
            Service.unsubscribe_user_from_station(user_id, station_id)
        except DoesNotExist:
            raise ValidationError("Invalid user and/or weather station id!")
        print("User unsubscribed successfully")
