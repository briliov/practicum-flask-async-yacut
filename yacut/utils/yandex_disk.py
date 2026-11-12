"""Module for asynchronous work with the Yandex.Disk API."""

import asyncio
from http import HTTPStatus

import aiohttp
from werkzeug.datastructures import FileStorage

from .. import app
from .exceptions import (
    GetDowloadURLError,
    UploadFailureError,
    UploadURLNotFoundError,
    YandexDiskError,
)

YANDEX_DISK_AUTH_TOKEN = app.config['YANDEX_DISK_AUTH_TOKEN']
UPLOAD_URL_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
DOWNLOAD_URL_ENDPOINT = (
    'https://cloud-api.yandex.net/v1/disk/resources/download'
)


async def get_url_for_upload(
    session: aiohttp.ClientSession,
    path: str,
) -> str:
    """Async returns a link to download a file."""
    async with session.get(
        UPLOAD_URL_ENDPOINT,
        params={
            'path': path,
            'overwrite': 'true',
        },
    ) as response:
        if response.status != HTTPStatus.OK:
            error_text = await response.text()
            raise UploadURLNotFoundError(
                f'Яндекс вернул {response.status}: {error_text}',
            )
        data = await response.json()
        if not (href := data.get('href')):
            raise UploadURLNotFoundError('Яндекс не вернул ссылку.')
        return href


async def upload_file_by_url(
    session: aiohttp.ClientSession,
    file_bytes: bytes,
    url_for_upload: str,
) -> None:
    """Async upload a file bytes from a link."""
    async with session.put(
        url_for_upload,
        data=file_bytes,
    ) as response:
        if response.status not in (HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
            error_text = await response.text()
            raise UploadFailureError(
                f'Яндекс вернул {response.status}: {error_text}',
            )


async def get_url_for_download(
    session: aiohttp.ClientSession,
    path: str,
) -> str:
    """Returns a url for download file."""
    async with session.get(
        DOWNLOAD_URL_ENDPOINT,
        params={'path': path},
    ) as response:
        if response.status != HTTPStatus.OK:
            error_text = await response.text()
            raise GetDowloadURLError(
                f'Яндекс вернул {response.status}: {error_text}',
            )
        data = await response.json()
        if not (href := data.get('href')):
            raise GetDowloadURLError('Яндекс не вернул ссылку.')
        return href


async def process_file(
    session: aiohttp.ClientSession,
    file: FileStorage,
) -> dict:
    """Async algorithm for saving a file on YandexDisk and
    obtaining a link to it."""
    if not file or not file.filename:
        return {
            'filename': 'Неизвестный файл',
            'error': 'Файл пуст или не передан.',
        }

    file_name = file.filename
    path = f'app:/{file_name}'  # type: ignore
    file_bytes: bytes = file.read()

    try:
        url_for_upload: str = await get_url_for_upload(
            session=session,
            path=path,
        )

        await upload_file_by_url(
            session=session,
            file_bytes=file_bytes,
            url_for_upload=url_for_upload,
        )

        url_for_download: str = await get_url_for_download(
            session=session,
            path=path,
        )

        return {'file_name': file_name, 'file_url': url_for_download}
    except (
        YandexDiskError,
        aiohttp.ClientError,
        asyncio.TimeoutError,
    ) as error:
        return {'file_name': file_name, 'error': str(error)}


async def upload_files_to_yandex_disk(files: list) -> list[dict[str, str]]:
    """Async upload files and return url for download."""
    if not files:
        raise YandexDiskError(
            'The file list is empty. Loading is not possible.',
        )
    async with aiohttp.ClientSession(
        headers={
            'Authorization': f'OAuth {YANDEX_DISK_AUTH_TOKEN}',
        },
    ) as session:
        tasks = [
            asyncio.create_task(process_file(session, file)) for file in files
        ]
        return await asyncio.gather(*tasks)
