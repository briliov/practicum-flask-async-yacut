from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLCreateForm(FlaskForm):
    original_link = URLField(
        'Добавьте оригинальную ссылку',
        validators=[DataRequired(message='Ссылка для сокращение обязательна')],
    )
    custom_id = StringField(
        'Добавьте кастомную сокращенную ссылку',
        validators=[Optional(), Length(1, 16)],
    )
    submit = SubmitField('Создать')


class URlDownloadFileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы для загрузки',
        validators=[DataRequired(message='Загрузите хотя бы один файл')],
    )
    submit = SubmitField('Загрузить')
