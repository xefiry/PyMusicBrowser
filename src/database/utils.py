"""Various functions to parse data from songs metadata"""

from datetime import datetime
from io import BytesIO
from peewee import CharField, IntegerField

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3


def get_str(data: EasyID3, key: str, value_if_none: str | None = None) -> str | None:
    value = data.get(key)

    if value is None:
        return value_if_none
    else:
        return value[0]


def get_numbers(data: EasyID3, key: str) -> tuple[int | None, int | None]:
    value = data.get(key)

    if value is None:
        return (None, None)

    split = value[0].split("/")

    if len(split) == 1:
        return (split[0], None)
    else:
        return (split[0], split[1])


def get_year(data: EasyID3, key: str) -> int | None:
    value = data.get(key)

    if value is None:
        return None

    value = value[0]

    if value.isnumeric():
        return int(value)

    try:
        date = datetime.strptime(value, "%Y-%m-%d")
        return date.year
    except ValueError:
        return None


def get_cover(file_path: str) -> BytesIO | None:
    tag = ID3(file_path)
    pic = tag.get("APIC:")
    if pic is not None:
        pic = BytesIO(pic.data)

    return pic


def match_str(db_field: CharField, input: str) -> bool:
    # ToDo: ignore accentuated characters
    return input.lower() in str(db_field).lower()


def match_int(db_field: IntegerField, input: str) -> bool:
    return input in str(db_field)
