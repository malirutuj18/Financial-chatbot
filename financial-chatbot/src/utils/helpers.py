"""Helper utility functions"""

import re


def format_currency(amount: float) -> str:
    """Format number as readable currency"""
    try:
        if amount >= 1e12:
            return f"${amount/1e12:.2f}T"
        elif amount >= 1e9:
            return f"${amount/1e9:.2f}B"
        elif amount >= 1e6:
            return f"${amount/1e6:.2f}M"
        elif amount >= 1e3:
            return f"${amount/1e3:.2f}K"
        else:
            return f"${amount:.2f}"
    except:
        return "N/A"


def validate_ticker(ticker: str) -> bool:
    """Validate ticker symbol format (1-5 uppercase letters)"""
    if not ticker:
        return False
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, ticker.upper()))
