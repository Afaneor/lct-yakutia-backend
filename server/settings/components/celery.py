from django.conf import settings

from server.settings.components import config

CELERY = {
    'broker_url': config(
        'CELERY_BROKER_URL',
        default='amqp://guest:guest@rabbitmq:5672/',
        cast=str,
    ),
    'task_always_eager': settings.TESTING,  # type: ignore
    'worker_hijack_root_logger': False,
    'timezone': settings.TIME_ZONE,
}
