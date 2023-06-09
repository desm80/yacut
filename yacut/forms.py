from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    """
    Форма для шаблона.
    """
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Необходимо ввести ссылку'),
                    Length(1, 256)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16),
                    Optional(),
                    Regexp(regex=r'^[a-zA-Z0-9]*\Z',
                           message='Неверные символы'),
                    ]
    )
    submit = SubmitField('Создать')
