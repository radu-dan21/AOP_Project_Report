from src.domain import MODELS, db


def create_tables():
    db.create_tables(MODELS)


def delete_tables():
    db.drop_tables(MODELS)
