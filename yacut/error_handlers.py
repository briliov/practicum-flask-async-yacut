from http import HTTPStatus

from flask import jsonify, render_template, request

from . import app, db


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str, status_code=None) -> None:
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error: HTTPStatus):
    if request.path.startswith('/api/'):
        return jsonify(
            {'message': 'Указанный id не найден'},
        ), HTTPStatus.NOT_FOUND
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(error: HTTPStatus):
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify(
            {'message': 'Внутренняя ошибка сервера'},
        ), HTTPStatus.INTERNAL_SERVER_ERROR
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
