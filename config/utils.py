def to_bool(value: str | None) -> bool:
    return (value or '').lower() in ('1', 'true')


def to_list(value: str | None, separator: str = ',') -> list[str]:
    return value.split(separator) if value else []
