import requests
from django.conf import settings


def get_request_for_get_marketing_text(
    prompt: str
):
    return requests.post(
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
