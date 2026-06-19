from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class MainForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')],
        render_kw={'placeholder': 'Длинная ссылка'})
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=16),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Допустимы только латинские буквы и цифры.')],
        render_kw={
            'placeholder': 'Ваш вариант короткой ссылки'})
    submit = SubmitField('Создать')


class LoadForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Загрузить')