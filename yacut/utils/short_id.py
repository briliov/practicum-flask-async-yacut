"""
Module for generating unique short IDs.

Uses a random selection of Latin characters and numbers.
Checks the uniqueness of the generated ID in the database.
"""

import random
import string

from ..models import URLMap


def get_unique_short_id(length=6):
    """Returns a short unique ID."""
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
