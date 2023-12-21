import re


def float_formatter(value) -> float | None:
    """
    Converts a string value into a float after cleaning non-numeric characters.

    Args:
    - value (str): The input string value that potentially contains numeric characters.

    Returns:
    - float or None: Returns the cleaned numeric value as a float if it exists, otherwise returns None.

    Example:
    >>> float_formatter("$1,234.56")
    1234.56
    >>> float_formatter("Not a numeric value")
    None
    """
    cleaned_price = re.sub(r'[^\d.]', '', value)
    return float(cleaned_price) if cleaned_price else None

