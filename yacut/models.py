"""Models for YaCut project."""

from datetime import datetime

from . import db


class URLMap(db.Model):
    """Model for mapping urls."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def is_short_id_taken(short_id: str) -> bool:
        """Checks whether such a short ID already exists in the database."""
        return URLMap.query.filter_by(short=short_id).first() is not None
