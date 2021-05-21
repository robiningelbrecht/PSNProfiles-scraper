def to_int(a: str) -> int:
    try:
        return int(a.replace(",", ""))
    except ValueError:
        return 0
