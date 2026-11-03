from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLCreateForm(FlaskForm):
    original_link = URLField(
        'Добавьте оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле')],
    )
    custom_id = StringField(
        'Добавьте кастомную сокращенную ссылку',
        validators=[Optional(), Length(1, 16)],
    )
    submit = SubmitField('Создать')
