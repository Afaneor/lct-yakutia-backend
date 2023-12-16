import requests
from django.conf import settings
from rest_framework import status

from server.apps.llm_request.models import Message
from server.apps.services.enums import MessageType
from server.celery import app


class SendException(Exception):  # noqa: N818
    """Сервис с llm_model не доступен."""


class ApiException(Exception):  # noqa: N818
    """Некорректная отправка данных в llm_model."""


@app.task(bind=True)
def send_request_for_get_marketing_text(
    self,
    prompt: str,
    user_request_id: int,
):
    """Отправить запрос в llm_model"""
    response = requests.post(
        url=f'{settings.LLM_MODEL_URL_FOR_GENERATE_MARKETING_TEXT}',
        json={
            'messages': [
                {
                    'content': settings.LLM_MODEL_SYSTEM_CONTENT_FOR_GENERATE_MARKETING_TEXT,
                    'role': 'system',
                },
                {
                    'content': (
                        settings.LLM_MODEL_USER_CONTENT_FOR_GENERATE_MARKETING_TEXT +
                        ' ' +
                        prompt,
                    ),
                    'role': 'user',
                }
            ],
        },
        timeout=60,
    )

    try:
        if response.status_code == status.HTTP_200_OK:
            answer = response.json()['choices'][0]['message']['content']

            Message.objects.create(
                user_request_id=user_request_id,
                text=answer,
                message_type=MessageType.SYSTEM,
            )

        elif str(response.status_code)[0] == '5':
            raise SendException(
                'Данные не отправлены. Код: {0}. Ошибка: {1}'.format(
                    response.status_code,
                    response.text,
                ),
            )

        else:
            raise ApiException(
                'Данные не отправлены. Код: {0}. Ошибка: {1}'.format(
                    response.status_code,
                    response.text,
                ),
            )

    except SendException as exc:
        raise self.retry(
            exc=exc,
            countdown=30,
            max_retries=5,
        )


@app.task(bind=True)
def send_request_for_get_channel_advice(
    self,
    prompt: str,
    user_request_id: int,
):
    """Отправить запрос в llm_model"""
    response = requests.post(
        url=f'{settings.LLM_MODEL_URL_FOR_GET_CHANNEL_ADVICE}',
        json={
            'messages': [
                {
                    'content': settings.LLM_MODEL_SYSTEM_CONTENT_FOR_GET_CHANNEL_ADVICE,
                    'role': 'system',
                },
                {
                    'content': (
                        settings.LLM_MODEL_USER_CONTENT_FOR_GET_CHANNEL_ADVICE +
                        ' ' +
                        prompt,
                    ),
                    'role': 'user',
                }
            ],
        },
        timeout=60,
    )

    try:
        if response.status_code == status.HTTP_200_OK:
            answer = response.json()['choices'][0]['message']['content']

            Message.objects.create(
                user_request_id=user_request_id,
                text=answer,
                message_type=MessageType.SYSTEM,
            )

        elif str(response.status_code)[0] == '5':
            raise SendException(
                'Данные не отправлены. Код: {0}. Ошибка: {1}'.format(
                    response.status_code,
                    response.text,
                ),
            )

        else:
            raise ApiException(
                'Данные не отправлены. Код: {0}. Ошибка: {1}'.format(
                    response.status_code,
                    response.text,
                ),
            )

    except SendException as exc:
        raise self.retry(
            exc=exc,
            countdown=30,
            max_retries=5,
        )
