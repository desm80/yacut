from http import HTTPStatus

from flask import abort, redirect, render_template

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import validate_or_create_short_id


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    """
    Рендеринг формы и обработка запроса на сохранение короткой ссылки в БД.
    """
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = validate_or_create_short_id(form.custom_id.data)
        if URLMap.query.filter_by(
                short=short_id).first() is not None:
            return render_template(
                'yacut.html', form=form, message=f'Имя {short_id} уже занято!'
            )
        urlmap = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(urlmap)
        db.session.commit()
        message = "http://localhost/" + short_id
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
    abort(HTTPStatus.NOT_FOUND)
