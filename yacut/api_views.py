import re

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if len(data) == 1:
        if 'url' not in data:
            raise InvalidAPIUsage('\"url\" является обязательным полем!', 400)
    for key in data.keys():
        if key not in ['url', 'custom_id']:
            raise InvalidAPIUsage('Неверный запрос', 400)
    if ('custom_id' not in data or data['custom_id'] == ''
            or data['custom_id'] is None):
        data['custom_id'] = get_unique_short_id()
    if len(data['custom_id']) > 16 or not re.match(r'^[a-zA-Z0-9]*\Z',
                                                   data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки', 400
        )

    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(f"Имя \"{data['custom_id']}\" уже занято.", 400)
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict_create()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify(url.to_dict_get())
    raise InvalidAPIUsage('Указанный id не найден', 404)
