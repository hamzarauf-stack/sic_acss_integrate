from datetime import datetime
from email_validator import validate_email, EmailNotValidError


def validate_date_format(date_string: str) -> str:
    """Validate the date format (YYYY-MM-DD).

    Args:
        date_string (str): The date string to validate.

    Returns:
        str: The validated date string in YYYY-MM-DD format.

    Raises:
        ValueError: If the date is not in the correct format.
    """
    try:
        # Attempt to parse the date string
        valid_date = datetime.strptime(date_string, "%Y-%m-%d")
        return valid_date.date().isoformat()  # Return date in YYYY-MM-DD format
    except ValueError:
        raise ValueError(
            "Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
