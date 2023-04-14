import random

from flask import abort, redirect, render_template

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.settings import LETTERS_NUMBERS, SHORT_LINK_LENGTH


def get_unique_short_id():
    """
    Создание уникальной короткой ссылки.
    """
    short_id = ''
    for i in range(int(SHORT_LINK_LENGTH)):
        short_id += random.choice(list(LETTERS_NUMBERS))
    if URLMap.query.filter_by(short=short_id).first():
        return get_unique_short_id()
    return short_id


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    """
    Рендеринг формы и обработка запроса на сохранение короткой ссылки в БД.
    """
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data == '' or form.custom_id.data is None:
            form.custom_id.data = get_unique_short_id()
        if URLMap.query.filter_by(
                short=form.custom_id.data).first() is not None:
            return render_template('yacut.html', form=form, message=f'Имя {form.custom_id.data} уже занято!')
        urlmap = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(urlmap)
        db.session.commit()

        message = "http://localhost/" + form.custom_id.data
        form.custom_id.data = ''
        return render_template('yacut.html', form=form, message=message)
    return render_template('yacut.html', form=form)


@app.route('/<string:short_id>')
def opinion_view(short_id):
    """
    Функция переадресации по короткой ссылке на исходную страницу.
    """
    url = URLMap.query.filter_by(short=short_id).first()
    if url is not None:
        return redirect(url.original)
    abort(404)
