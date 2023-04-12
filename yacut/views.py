from flask import render_template

from yacut import app
from yacut.forms import URLMapForm


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    return render_template('index.html', form=form)
