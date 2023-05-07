from peewee import CharField, Model
from playhouse.shortcuts import model_to_dict
from src.domain.db import db


class ValidationError(Exception):
    ...


class BaseModel(Model):
    class Meta:
        database = db

    name = CharField(unique=True)

    def save(self, force_insert=False, only=None):
        self.clean()
        super().save(force_insert=force_insert, only=only)

    def clean(self) -> None:
        self.clean_name()

    def clean_name(self):
        name = self.name
        if not isinstance(name, str):
            raise ValidationError("Name should be a non-empty string!")
        name: str = name.strip()
        if not name:
            raise ValidationError("Name can't be empty!")
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}{model_to_dict(self)}"
