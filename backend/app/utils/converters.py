def str_to_bool(value: str) -> bool:
    value = value.strip().lower()
    if value in ('true', '1', "yes", 'y'):
        return True
    elif value in ('false', '0', 'no', 'n'):
        return False
    raise ValueError(f"Invalid boolean string: {value}")