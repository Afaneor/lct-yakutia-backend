import requests
from django.conf import settings
from rest_framework import status

from server.apps.llm_request.models import Message, RequestData
from server.apps.llm_request.services.exception import (
    ApiException,
    SendException,
)
from server.apps.llm_request.services.formation_request import (
    get_request_for_get_marketing_text,
)
from server.apps.services.enums import MessageType, RequestStatus
from server.celery import app


@app.task(bind=True)
def celery_send_request_for_get_marketing_text(
    self,
    prompt: str,
    request_data_id: int,
    message_id: int,
):
    """Отправить запрос в llm_model через celery."""
    response = get_request_for_get_marketing_text(prompt=prompt)
    request_data = RequestData.objects.get(id=request_data_id)

    try:
        if response.status_code == status.HTTP_200_OK:
            answer = response.json()['choices'][0]['message']['content']

            Message.objects.create(
                request_data_id=request_data_id,
                parent_id=message_id,
                text=answer,
                message_type=MessageType.SYSTEM,
            )
            request_data.status = RequestStatus.OK
            request_data.save()

        elif str(response.status_code)[0] == '5':
            request_data.status = RequestStatus.ERROR
            request_data.save()
            raise SendException(
                'Данные не отправлены. Код: {0}. Ошибка: {1}'.format(
                    response.status_code,
                    response.text,
                ),
            )

        else:
            request_data.status = RequestStatus.ERROR
            request_data.save()
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
    request_data_id: int,
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
                request_data_id=request_data_id,
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
