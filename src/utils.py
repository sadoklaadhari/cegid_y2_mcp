#!/usr/bin/env python3
"""
Utilities - Helper functions
"""

import logging
import html
import re
from typing import Any, Dict
from pathlib import Path

# Configure logging
def setup_logging(name: str) -> logging.Logger:
    """Setup logging for module"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger


def sanitize_input(value: Any) -> Any:
    """Sanitize user input to prevent injection attacks"""
    if isinstance(value, str):
        # Remove potentially dangerous characters
        value = html.escape(value)
        # Remove SQL injection patterns
        value = re.sub(r'([;\\\\])', '', value)
        return value
    elif isinstance(value, dict):
        return {k: sanitize_input(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [sanitize_input(v) for v in value]
    return value


def validate_email(email: str) -> bool:
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """Validate date format"""
    try:
        from datetime import datetime
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency"""
    return f"{currency} {amount:,.2f}"


def get_nested(data: Dict, path: str, default=None) -> Any:
    """Get nested dict value using dot notation"""
    keys = path.split(".")
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default
    return value if value is not None else default


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    for key, value in dict2.items():
        if isinstance(value, dict) and key in result:
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def batch_list(lst: list, batch_size: int) -> list:
    """Batch a list into chunks"""
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]


def truncate_string(s: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length"""
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


logger = setup_logging(__name__)
