from datetime import datetime


def parse_date(date_str):
    """Try to parse a date string in various formats."""
    formats = [
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%d/%m/%Y",
        "%d %B %Y",
        "%d %B",
        "%Y/%m/%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    return None


def clean_price(price_str):
    """Clean price string."""
    if not price_str:
        return None
    price_str = price_str.strip()
    if price_str.lower() in ("бесплатно", "free", "вход свободный"):
        return "Бесплатно"
    return price_str
