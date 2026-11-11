"""Models for YaCut project."""

from datetime import datetime

from . import db


class URLMap(db.Model):
    """Model for mapping urls."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
