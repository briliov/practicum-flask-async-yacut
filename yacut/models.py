"""Models for YaCut project."""

from datetime import datetime
import re

from flask import url_for
from sqlalchemy.orm import validates

from . import db
from .utils.constants import (
    MAX_CUSTOM_ID_LENGTH,
    MIN_CUSTOM_ID_LENGTH,
    RESERVED_SHORT_IDS,
)


class URLMap(db.Model):
    """Model for mapping urls."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_CUSTOM_ID_LENGTH),
        nullable=False,
        unique=True,
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def create(original: str, short: str):
        """Creates a new short link and saves it to the database."""
        if URLMap.is_short_taken(short):
            raise ValueError(
                'Предложенный вариант короткой ссылки уже существует.',
            )
        url_map: URLMap = URLMap(original=original, short=short)  # type: ignore
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @validates('short')
    def validate_short(self, key, value):
        """Automatically checks the ID format on any assignment."""
        if not value:
            raise ValueError('Короткий ID обязателен для заполнения.')
        if not (MIN_CUSTOM_ID_LENGTH <= len(value) <= MAX_CUSTOM_ID_LENGTH):
            raise ValueError('Указано недопустимое имя для короткой ссылки.')
        if not re.match(r'^[a-zA-Z0-9]+$', value):
            raise ValueError('Указано недопустимое имя для короткой ссылки.')
        return value

    @staticmethod
    def is_short_taken(short: str) -> bool:
        """Проверяет уникальность ID (в базе и среди зарезервированных)."""
        return (
            short in RESERVED_SHORT_IDS
            or URLMap.query.filter_by(short=short).first() is not None
        )

    @staticmethod
    def get_original_link(short: str) -> str:
        """Returns original url by short id."""
        url_map: URLMap = URLMap.query.filter_by(short=short).first_or_404()
        return url_map.original

    @staticmethod
    def get_short_link(short: str) -> str:
        """Returns short url by short id."""
        short_url: str = url_for(
            'redirect_view',
            short_id=short,
            _external=True,
        )
        return short_url
