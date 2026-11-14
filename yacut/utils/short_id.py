"""
Module for generating unique short IDs.

Uses a random selection of Latin characters and numbers.
Checks the uniqueness of the generated ID in the database.
"""

import random

from ..models import URLMap
from .constants import CHARACTERS, MAX_ATTEMPTS, UNIQ_SHORT_ID_MAX_LENGTH
from .exceptions import ShortIDGenerationError


def get_unique_short(
    length=UNIQ_SHORT_ID_MAX_LENGTH,
    max_attempts=MAX_ATTEMPTS,
):
    """Returns a short unique ID."""
    for _ in range(max_attempts):
        short = ''.join(random.choices(CHARACTERS, k=length))
        if not URLMap.is_short_taken(short=short):
            return short
    raise ShortIDGenerationError(
        f'Не удалось сгенерировать уникальный ID за {max_attempts} попыток.',
    )
