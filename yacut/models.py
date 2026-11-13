"""Models for YaCut project."""

from datetime import datetime


from . import db
from .utils.constants import MAX_CUSTOM_ID_LENGTH, RESERVED_SHORT_IDS


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
    def get_original_link(id: str) -> str:
        """Returns orinale url by short id."""
        url_map: URLMap = URLMap.query.filter_by(short=id).first_or_404()
        return url_map.original

    @staticmethod
    def is_short_id_taken(short_id: str) -> bool:
    @staticmethod
    def is_short_id_taken(id: str) -> bool:
        """Checks whether such a short ID already exists in the database."""
        return (
            id in RESERVED_SHORT_IDS
            or URLMap.query.filter_by(short=id).first() is not None
        )
