from peewee import DoesNotExist
from src.domain import ValidationError
from src.service import Service
from src.ui.base import AbstractMenu, catch_validation_exception
from src.ui.common import get_weather_stations_and_subscribed_users


class WeatherStationMenu(AbstractMenu):
    @classmethod
    def _get_menu_options(cls) -> list[tuple[str, callable]]:
        return [
            ("Add station", cls._add_station),
            ("Get stations", cls._get_stations),
            ("Change station name", cls._update_name),
            ("Change station temperature", cls._update_temperature),
            ("Remove station", cls._delete_station),
            ("Get subscriptions", get_weather_stations_and_subscribed_users),
        ]

    @staticmethod
    def _input_float(
        prompt: str,
        exclusive_bounds: tuple[float | None, float | None] = (None, None),
    ) -> float:
        try:
            value = float(input(prompt))
        except ValueError:
            raise ValidationError("Input must be a float value!")

        lb, ub = exclusive_bounds
        if (lb is not None and value <= lb) or (ub is not None and value >= ub):
            raise ValidationError(f"Input must be a float value between ({lb}, {ub})")

        return value

    @classmethod
    @catch_validation_exception
    def _add_station(cls):
        cls._get_stations()
        name = cls._input_string("\nPlease enter station name: ")
        temperature = cls._input_float("Please enter station temperature: ")
        Service.add_weather_station(name, temperature)
        print("Weather station added successfully")

    @staticmethod
    def _get_stations():
        stations = Service.get_weather_stations()
        if not stations:
            print("\nThere are no weather stations!")
        else:
            print("\nWeather stations:")
            for s in stations:
                print(s)

    @classmethod
    @catch_validation_exception
    def _update_name(cls):
        cls._get_stations()

        station_id = cls._input_int("Please enter station id: ", (0, None))
        try:
            station = Service.get_weather_station(station_id)
        except DoesNotExist:
            raise ValidationError("Station does not exist!")

        name = cls._input_string("\nPlease enter station name: ")
        Service.update_weather_station(station_id, name, station.temperature)

        print("Station updated successfully")

    @classmethod
    @catch_validation_exception
    def _update_temperature(cls):
        get_weather_stations_and_subscribed_users()

        station_id = cls._input_int("\nPlease enter station id: ", (0, None))
        try:
            station = Service.get_weather_station(station_id)
        except DoesNotExist:
            raise ValidationError("Station does not exist!")

        temperature = cls._input_float("\nPlease enter station temperature: ")
        Service.update_weather_station(station_id, station.name, temperature)

        print("Station updated successfully")

    @classmethod
    @catch_validation_exception
    def _delete_station(cls):
        cls._get_stations()
        user_id = cls._input_int("Please enter station id: ", (0, None))
        Service.delete_weather_station(user_id)
        print("Station deleted successfully")
