import requests
from django.conf import settings


def get_request_for_get_marketing_text(
    prompt: str
):
    """Корректный запрос в llm_model."""
    return requests.post(
        url=f'{settings.LLM_MODEL_URL_FOR_GENERATE_MARKETING_TEXT}',
        json={
            'messages': [
                {
                    'content': (
                        '<s>{system}\n{' +
                        f'{settings.LLM_MODEL_SYSTEM_CONTENT_FOR_GENERATE_MARKETING_TEXT}' +
                        f'{prompt}' +
                        '}</s>\n' +
                        '<s>{user}\n{' +
                        f'{settings.LLM_MODEL_USER_CONTENT_FOR_GENERATE_MARKETING_TEXT} ' +
                        '}</s>\n'
                    ),
                    'role': 'user',
                },
            ],
        },
        timeout=300,
    )
