from datetime import datetime

from yacut import db

API_NAMES = {
    'url': 'original',
    'custom_id': 'short',
}


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict_create(self):
        return dict(
            url=self.original,
            short_link='http://localhost/' + self.short,
        )

    def to_dict_get(self):
        return dict(
            url=self.original,
        )

    def from_dict(self, data):
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self, API_NAMES[field], data[field])
