"""Various functions to parse data from songs metadata"""

from datetime import datetime
from io import BytesIO

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


def s_to_t(seconds: float) -> str:
    """Convert a number of seconds to displayable time"""
    result: str = ""

    h = seconds // 3600
    seconds = seconds % 3600

    s = int(seconds % 60)
    m = int(seconds // 60)

    if h > 0:
        result = f"{h}:{m:02}:{s:02}"
    elif m > 0:
        result = f"{m}:{s:02}"
    else:
        result = str(s)

    return result
