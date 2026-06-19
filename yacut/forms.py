from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import REGEX, SHORT_ID_MAX_LENGTH, URL_MAX_LENGHT


class MainForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(DataRequired(message='Обязательное поле'),
                    Length(max=URL_MAX_LENGHT)),
        render_kw={'placeholder': 'Длинная ссылка'})
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Optional(),
            Length(max=SHORT_ID_MAX_LENGTH),
            Regexp(REGEX,
                   message='Допустимы только латинские буквы и цифры.')),
        render_kw={
            'placeholder': 'Ваш вариант короткой ссылки'})
    submit = SubmitField('Создать')


class LoadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[
            DataRequired(message='Выберите хотя бы один файл')])
    submit = SubmitField('Загрузить')
