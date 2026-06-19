import random
import string
from datetime import datetime
from re import fullmatch

from flask import url_for
from sqlalchemy.exc import IntegrityError

from . import db
from .constants import (ATTEMPTS, REGEX, RESERVED_SHORTS, SHORT_ID_LENGTH,
                        SHORT_ID_MAX_LENGTH, URL_MAX_LENGHT)
from .exceptions import ObjectCreateError, ShortGenerateError


class URLMap(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    original = db.Column(db.String(URL_MAX_LENGHT),
                         nullable=False)
    short = db.Column(db.String(SHORT_ID_MAX_LENGTH),
                      unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url())

    @classmethod
    def create(cls, original, short=None):
        """Создать и сохранить новую запись."""

        if short:
            if (
                len(short) > SHORT_ID_MAX_LENGTH
                or not fullmatch(REGEX, short)
            ):
                raise ObjectCreateError(
                    'Указано недопустимое имя для короткой ссылки')
            if short in RESERVED_SHORTS:
                raise ObjectCreateError(
                    'Предложенный вариант короткой ссылки уже существует.')
            if cls.get(short):
                raise ObjectCreateError(
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
            raise ObjectCreateError(
                'Предложенный вариант короткой ссылки уже существует.')
        return url_map

    @classmethod
    def get_unique_short_id(cls):
        """Получить уникальный короткий идентификатор."""
        for _ in range(ATTEMPTS):
            short_id = ''.join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=SHORT_ID_LENGTH))
            if cls.get(short_id) is None:
                return short_id
        raise ShortGenerateError('Не удалось создать уникальный id')

    @classmethod
    def get(cls, short):
        """Получить запись по короткому идентификатору."""
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        return url_for(
            'short_view',
            short=self.short,
            _external=True)
