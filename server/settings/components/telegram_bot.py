from server.settings.components import config

TELEGRAM_BOT_TOKEN = config(
    'TELEGRAM_BOT_TOKEN',
    default='',
)
