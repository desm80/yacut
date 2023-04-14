from datetime import datetime

from yacut import db

API_NAMES = {
    'url': 'original',
    'custom_id': 'short',
}


class URLMap(db.Model):
    """
    Модель для создания коротких ссылок.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict_create(self):
        """
        Словарь для вывода результата создания ссылки в АПИ.
        """
        return dict(
            url=self.original,
            short_link='http://localhost/' + self.short,
        )

    def to_dict_get(self):
        """
        Словарь для вывода полной ссылки по запросу из короткой ссылки.
        """
        return dict(
            url=self.original,
        )

    def from_dict(self, data):
        """
        Обработка входящих данных из JSON для создания объекта URLMap.
        """
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self, API_NAMES[field], data[field])
