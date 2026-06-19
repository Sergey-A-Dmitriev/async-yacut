from http import HTTPStatus


class InvalidAPIUsage(Exception):
    """Класс исключений, возникающих в API."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class ObjectCreateError(Exception):
    """Ошибка создания объекта."""


class ShortGenerateError(Exception):
    """Ошибка создания объекта."""
