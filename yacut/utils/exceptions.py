"""Module with exceptions for project YaCut"""

from http import HTTPStatus


class YandexDiskError(Exception):
    """Basic error when working with Yandex.Disk."""


class UploadURLNotFoundError(YandexDiskError):
    """Failed to get download link."""


class UploadFailureError(YandexDiskError):
    """Error loading files to Yandex disk."""


class GetDowloadURLError(YandexDiskError):
    """Error receiving download link."""


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str, status_code=None) -> None:
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return dict(message=self.message)
