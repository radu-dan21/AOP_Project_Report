from peewee import IntegrityError, Model
from src.domain import User, UserStation, ValidationError, WeatherStation


class Service:
    def __init__(self, *args, **kwargs):
        ...

    @staticmethod
    def __create_entity(model: type[Model], **kwargs) -> None:
        try:
            model.create(**kwargs)
        except IntegrityError:
            raise ValidationError(f"{model.__name__} already exists!")

    @staticmethod
    def __get_entity_by_id(model: type[Model], entity_id: int) -> Model:
        return model.get_by_id(entity_id)

    @staticmethod
    def __get_all_entities(model: type[Model]) -> list[Model]:
        return list(model.select())

    @classmethod
    def __update_entity(cls, model: type[Model], entity_id: int, **kwargs) -> Model:
        entity: Model = cls.__get_entity_by_id(model, entity_id)

        for field_name, field_value in kwargs.items():
            setattr(entity, field_name, field_value)

        try:
            entity.save()
        except IntegrityError:
            raise ValidationError(f"{model.__name__} already exists!")

        return entity

    @staticmethod
    def __delete_entity(model: type[Model], entity_id: int) -> None:
        if not model.delete_by_id(entity_id):
            raise ValidationError(f"{model.__name} does not exist!")

    @classmethod
    def add_user(cls, name: str) -> None:
        cls.__create_entity(User, name=name)

    @classmethod
    def add_weather_station(cls, name: str, temperature: float | None = None) -> None:
        cls.__create_entity(WeatherStation, name=name, temperature=temperature)

    @classmethod
    def get_user(cls, user_id: int) -> User:
        return cls.__get_entity_by_id(User, user_id)

    @classmethod
    def get_weather_station(cls, weather_station_id: int) -> WeatherStation:
        return cls.__get_entity_by_id(WeatherStation, weather_station_id)

    @classmethod
    def get_users(cls) -> list[User]:
        return cls.__get_all_entities(User)

    @classmethod
    def get_weather_stations(cls) -> list[WeatherStation]:
        return cls.__get_all_entities(WeatherStation)

    @classmethod
    def update_user(cls, user_id: int, name: str) -> None:
        cls.__update_entity(User, user_id, name=name)

    @classmethod
    def update_weather_station(
        cls, weather_station_id: int, name: str, temperature: float | None = None
    ) -> None:
        weather_station: WeatherStation = cls.__update_entity(
            WeatherStation,
            weather_station_id,
            name=name,
        )
        if weather_station.temperature != temperature:
            weather_station.change_temp(temperature)

    @classmethod
    def delete_user(cls, user_id: int) -> None:
        cls.__delete_entity(User, user_id)

    @classmethod
    def delete_weather_station(cls, weather_station_id: int) -> None:
        cls.__delete_entity(WeatherStation, weather_station_id)

    @classmethod
    def subscribe_user_to_weather_station(
        cls,
        user_id: int,
        weather_station_id: int,
    ) -> None:
        user: User = cls.get_user(user_id)
        weather_station: WeatherStation = cls.get_weather_station(weather_station_id)

        try:
            weather_station.users.add(user)
        except IntegrityError:
            raise ValidationError("User already subscribed to weather station!")

    @classmethod
    def unsubscribe_user_from_station(
        cls,
        user_id: int,
        weather_station_id: int,
    ) -> None:
        user: User = cls.get_user(user_id)
        weather_station: WeatherStation = cls.get_weather_station(weather_station_id)

        if not weather_station.users.remove(user):
            raise ValidationError("User is not subscribed to weather station!")

    @classmethod
    def get_weather_stations_and_subscribed_users(
        cls,
    ) -> dict[WeatherStation, list[User]]:
        weather_stations: list[WeatherStation] = list(
            WeatherStation.select().left_outer_join(UserStation).left_outer_join(User)
        )
        return {ws: list(ws.users) for ws in weather_stations}
