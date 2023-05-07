from peewee import Check, FloatField, IntegrityError, ManyToManyField
from src.domain.models.base import BaseModel, ValidationError
from src.domain.models.user import User
from src.domain.observer import Publisher, Subscriber, changes_state


class WeatherStation(BaseModel, Publisher):
    MIN_TEMP: int = -100
    MAX_TEMP: int = 100

    temperature = FloatField(
        null=True,
        default=None,
        constraints=[
            Check(f"temperature > {MIN_TEMP}"),
            Check(f"temperature < {MAX_TEMP}"),
        ],
    )

    users = ManyToManyField(User, backref="stations")

    def clean(self) -> None:
        super().clean()
        self.clean_temperature()

    def clean_temperature(self) -> None:
        if self.temperature is None:
            return
        try:
            temperature = float(self.temperature)
            if temperature < self.MIN_TEMP or temperature > self.MAX_TEMP:
                raise ValidationError
        except Exception:
            raise ValidationError(
                f"Temperature should be a float value "
                f"between {self.MIN_TEMP} and {self.MAX_TEMP}"
            )

    def get_subscribers(self) -> list[Subscriber]:
        return list(self.users)

    def subscribe(self, subscriber: Subscriber) -> None:
        try:
            self.users.add(subscriber)
        except IntegrityError:
            pass

    def unsubscribe(self, subscriber: Subscriber) -> None:
        if not isinstance(subscriber, User):
            return
        self.users.remove(subscriber.id)

    def notify_subscribers(self, message: str | None = None) -> None:
        print(
            f"{self} - "
            f"Notifying {self.get_subscribers_count()} subscribers - "
            f"{message}"
        )
        super().notify_subscribers(message)

    def get_subscribers_count(self):
        return self.users.count()

    @changes_state("Changed temperature -> old value = {}")
    def change_temp(self, new_temp) -> float:
        old_temp: float = self.temperature
        if new_temp != old_temp:
            self.temperature = new_temp
            self.save()
        return old_temp


UserStation = WeatherStation.users.get_through_model()
