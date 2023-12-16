from decouple import config

ARGILLA_API_URL = config('ARGILLA_API_URL', default='')
ARGILLA_API_KEY = config('ARGILLA_API_KEY', default='admin.apikey')
