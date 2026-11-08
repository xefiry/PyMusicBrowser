import peewee

DATABASE_FILE = "library.db"


db = peewee.SqliteDatabase(DATABASE_FILE)


class BaseModel(peewee.Model):
    class Meta:
        database = db


def init(models) -> None:
    db.connect()
    db.create_tables(models)
    db.execute_sql("PRAGMA journal_mode = off;")
    db.execute_sql("PRAGMA synchronous = 0;")


def vacuum() -> None:
    db.execute_sql("VACUUM;")
