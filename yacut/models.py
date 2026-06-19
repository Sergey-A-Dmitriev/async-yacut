import random
import string
from datetime import datetime
from re import fullmatch

from sqlalchemy.exc import IntegrityError

from . import db
from .constants import (REGEX, RESERVED_SHORTS, SHORT_ID_LENGTH,
                        SHORT_ID_MAX_LENGTH)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    class ObjectCreateError(Exception):
        """Ошибка создания объекта."""
        pass

    class ShortGenerateError(Exception):
        """Ошибка создания объекта."""
        pass

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short)

    def from_dict(self, data):
        # Для каждого поля модели, которое можно заполнить...
        field = 'short'
        if field in data:
            # Если есть, добавить значение из словаря
            # в соответствующее поле объекта модели.
            setattr(self, field, data[field])

    @classmethod
    def create(cls, original, short=None):
        """Создать и сохранить новую запись."""

        if short:
            if (
                len(short) > SHORT_ID_MAX_LENGTH
                or not fullmatch(REGEX, short)
            ):
                raise cls.ObjectCreateError(
                    'Указано недопустимое имя для короткой ссылки')
            if short in RESERVED_SHORTS:
                raise cls.ObjectCreateError(
                    'Предложенный вариант короткой ссылки уже существует.')
            if cls.get(short):
                raise cls.ObjectCreateError(
                    'Предложенный вариант короткой ссылки уже существует.')
        else:
            short = cls.get_unique_short_id()
        url_map = cls(
            original=original,
            short=short)
        try:
            db.session.add(url_map)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise cls.ObjectCreateError(
                'Предложенный вариант короткой ссылки уже существует.')
        return url_map

    @classmethod
    def get_unique_short_id(cls):
        """Получить уникальный короткий идентификатор."""
        while True:
            short_id = ''.join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=SHORT_ID_LENGTH))
            if cls.get(short_id) is None:
                return short_id

    @classmethod
    def get(cls, short):
        """Получить запись по короткому идентификатору."""
        return URLMap.query.filter_by(short=short).first()