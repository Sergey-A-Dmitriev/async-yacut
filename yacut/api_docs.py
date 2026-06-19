from . import app

try:
    from swagger_ui import api_doc
    api_doc(app,
            config_path='./yacut/static/docs/openapi.yml',
            url_prefix='/doc')
except ImportError:
    pass
