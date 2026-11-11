"""Forms for YaCut project."""

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .models import URLMap
from .utils.constants import MAX_CUSTOM_ID_LENGTH, MIN_CUSTOM_ID_LENGTH


class URLCreateForm(FlaskForm):
    """Form for custom url for link."""

    original_link = URLField(
        'Добавьте оригинальную ссылку',
        validators=[DataRequired(message='Ссылка для сокращение обязательна')],
    )
    custom_id = StringField(
        'Добавьте кастомную сокращенную ссылку',
        validators=[
            Optional(),
            Length(MIN_CUSTOM_ID_LENGTH, MAX_CUSTOM_ID_LENGTH),
        ],
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data:
            if (
                URLMap.query.filter_by(short=field.data).first()
                or field.data == 'files'
            ):
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.',
                )


class URlUploadFileForm(FlaskForm):
    """Form for creating custom url for uploaded file."""

    files = MultipleFileField(
        'Выберите файлы для загрузки',
        validators=[DataRequired(message='Загрузите хотя бы один файл')],
    )
    submit = SubmitField('Загрузить')
