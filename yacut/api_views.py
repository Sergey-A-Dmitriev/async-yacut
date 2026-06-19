from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    """Получение оригинальной ссылки."""
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    """Создание короткой ссылки."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidAPIUsage('"url" является обязательным полем!')
    try:
        url_map = URLMap.create(
            data['url'],
            data.get('custom_id'))

        return jsonify(
            {
                'url': url_map.original,
                'short_link': request.host_url + url_map.short
            }
        ), HTTPStatus.CREATED
    except (URLMap.ObjectCreateError, URLMap.ShortGenerateError) as exc:
        raise InvalidAPIUsage(str(exc))