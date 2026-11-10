"""API for project YaCut"""

from http import HTTPStatus
import re

from flask import jsonify, request, url_for

from . import app, db
from .constants import MAX_CUSTOM_ID_LENGTH, MIN_CUSTOM_ID_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils.short_id import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not (url := data.get('url')):
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if custom_id := data.get('custom_id'):
        if (
            not isinstance(custom_id, str)
            or (
                len(custom_id)
                not in range(MIN_CUSTOM_ID_LENGTH, MAX_CUSTOM_ID_LENGTH + 1)
            )
            or (not re.match(r'^[a-zA-Z0-9]+$', custom_id))
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
            )
        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
            )
    else:
        custom_id = get_unique_short_id()
    url_map: URLMap = URLMap(
        original=url,  # type: ignore
        short=custom_id,  # type: ignore
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify(
        {
            'url': url,
            'short_link': url_for(
                'redirect_view',
                short_id=custom_id,
                _external=True,
            ),
        },
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id: str):
    if not (url_map := URLMap.query.filter_by(short=short_id).first()):
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify(
        {
            'url': url_map.original,
        },
    ), HTTPStatus.OK
