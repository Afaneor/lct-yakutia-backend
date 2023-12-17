from server.settings.components import config

ARGILLA_API_URL = config('ARGILLA_API_URL', default='http://argilla:6900/')
ARGILLA_API_KEY = config('ARGILLA_API_KEY', default='admin.apikey')
ARGILLA_WORKSPACE = config('ARGILLA_WORKSPACE', default='admin')
