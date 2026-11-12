RATES = {"DOM": 3, "COM": 6}
SLAB = {"A": 1, "B": 2}

MAX_DIGITS = 12   # reject absurdly large numbers (avoids overflow / DoS)


def _parse_units(text):
    """Strictly parse a non-negative integer made of ASCII digits only.

    Returns an int, or None if `text` is not a valid reading.
    Rejects: non-strings, '', '-5', '+5', '1.5', '1_000', unicode digits,
    and numbers longer than MAX_DIGITS.
    """
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not text or len(text) > MAX_DIGITS:
        return None
    if not (text.isascii() and text.isdigit()):
        return None
    return int(text)


def units_consumed(reading):
    """'previous:current' -> units used, or None if the input is invalid."""
    if not isinstance(reading, str):
        return None
    parts = reading.split(':')
    if len(parts) != 2:
        return None
    previous, current = _parse_units(parts[0]), _parse_units(parts[1])
    if previous is None or current is None:
        return None
    if current < previous:          # meter cannot run backwards
        return None
    return current - previous


def daily_average(units_csv):
    """'5,7,6' -> average (2 dp), or None if the input is invalid."""
    if not isinstance(units_csv, str):
        return None
    units = [_parse_units(u) for u in units_csv.split(',')]
    if not units or any(u is None for u in units):   # catches '' and '1,,3'
        return None
    return round(sum(units) / len(units), 2)


def tariff_rate(code):
    """'DOM-A' -> rate per unit, or None if the code is invalid."""
    if not isinstance(code, str):
        return None
    parts = code.strip().upper().split('-')
    if len(parts) != 2:
        return None
    category, slab = parts
    if category not in RATES or slab not in SLAB:
        return None
    return RATES[category] * SLAB[slab]


def main():
    print("==== Running units_consumed ====")
    user_input = input("Enter meter readings as previous:current (e.g. 1200:1350): ")
    result = units_consumed(user_input)
    print("Units Consumed:", result if result is not None else "Invalid input")

    print("\n==== Running daily_average ====")
    user_input = input("Enter daily units as CSV (e.g. 5,7,6): ")
    result = daily_average(user_input)
    print("Daily Average:", result if result is not None else "Invalid input")

    print("\n==== Running tariff_rate ====")
    user_input = input("Enter a tariff code (e.g. DOM-A): ")
    result = tariff_rate(user_input)
    print("Rate per Unit:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
