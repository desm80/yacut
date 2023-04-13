import random
from urllib.parse import urljoin

from flask import render_template, redirect, url_for, session, request, flash

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.settings import BASE_URL, SHORT_LINK_LENGTH, LETTERS_NUMBERS


def get_unique_short_id():
    short_id = ''
    for i in range(int(SHORT_LINK_LENGTH)):
        short_id += random.choice(list(LETTERS_NUMBERS))
    if URLMap.query.filter_by(short=short_id).first():
        return get_unique_short_id()
    return short_id


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data == '':
            form.custom_id.data = get_unique_short_id()
        urlmap = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(urlmap)
        db.session.commit()
        message = urljoin(BASE_URL, form.custom_id.data)
        form.custom_id.data = ''
        return render_template('yacut.html', form=form, message=message)
    return render_template('yacut.html', form=form)

