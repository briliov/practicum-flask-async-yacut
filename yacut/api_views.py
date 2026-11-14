"""API for project YaCut"""

from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .models import URLMap
from .utils.exceptions import InvalidAPIUsage
from .utils.short import get_unique_short


@app.route('/api/id/', methods=['POST'])
def create_id():
    """Creates a new short link via the API."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not (original := data.get('url')):
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short: str = data.get('custom_id') or get_unique_short()
    try:
        url_map: URLMap = URLMap.create(original=original, short=short)
        return jsonify(
            {
                'url': original,
                'short_link': url_for(
                    'redirect_view',
                    short=url_map.short,
                    _external=True,
                ),
            },
        ), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(str(error), HTTPStatus.BAD_REQUEST)


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short: str):
    """Returns the original link by short ID."""
    original = URLMap.get_original_link(short=short)
    if not original:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': original}), HTTPStatus.OK
