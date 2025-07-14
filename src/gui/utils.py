def s_to_t(seconds: float) -> str:
    """Convert a number of seconds to displayable time"""
    result: str = ""

    h = seconds // 3600
    seconds = seconds % 3600

    s = int(seconds % 60)
    m = int(seconds // 60)

    if h > 0:
        result = f"{h}:{m:02}:{s:02}"
    else:
        result = f"{m}:{s:02}"

    return result
