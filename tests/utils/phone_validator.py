import re
from tests.utils.constants import ERR_INVALID_PHONE

def normalize_phone_number(phone: str) -> str:
    """Normalize phone number to standard +62 format."""
    if not phone:
        raise ValueError(ERR_INVALID_PHONE)

    cleaned = phone.strip()
    
    # Check if input contains invalid non-numeric/plus characters
    if not re.match(r'^\+?[0-9]+$', cleaned):
        raise ValueError(ERR_INVALID_PHONE)

    # Check for invalid all-zero strings
    if re.match(r'^0+$', cleaned) or re.match(r'^\+620+$', cleaned):
        raise ValueError(ERR_INVALID_PHONE)

    if cleaned.startswith("+62"):
        national_num = cleaned[3:]
    elif cleaned.startswith("08"):
        national_num = cleaned[1:]
    else:
        raise ValueError(ERR_INVALID_PHONE)

    # Valid national length (8-11 digits after 8, making 08x 10-13 digits total)
    if not (8 <= len(national_num) <= 11):
        raise ValueError(ERR_INVALID_PHONE)

    return f"+62{national_num}"