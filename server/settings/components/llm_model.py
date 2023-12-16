from decouple import config

LLM_MODEL_URL_FOR_GENERATE_MARKETING_TEXT = config(
    'LLM_MODEL_URL_FOR_GENERATE_MARKETING_TEXT',
    default='localhost/v1/chat/completions'
)


LLM_MODEL_URL_FOR_GET_CHANNEL_ADVICE = config(
    'LLM_MODEL_URL_FOR_GET_CHANNEL_ADVICE',
    default='localhost/v1/chat/completions'
)


LLM_MODEL_SYSTEM_CONTENT_FOR_GENERATE_MARKETING_TEXT = config(
    'LLM_MODEL_SYSTEM_CONTENT_FOR_GENERATE_MARKETING_TEXT',
    default='Все ответы должны быть на русском.'
)


LLM_MODEL_USER_CONTENT_FOR_GENERATE_MARKETING_TEXT = config(
    'LLM_MODEL_USER_CONTENT_FOR_GENERATE_MARKETING_TEXT',
    default='Напиши маркетинговое предложение на русском языке учитывая.',
)

LLM_MODEL_SYSTEM_CONTENT_FOR_GET_CHANNEL_ADVICE = config(
    'LLM_MODEL_SYSTEM_CONTENT_FOR_GET_CHANNEL_ADVICE',
    default='Все ответы должны быть на русском.'
)


LLM_MODEL_USER_CONTENT_FOR_GET_CHANNEL_ADVICE = config(
    'LLM_MODEL_USER_CONTENT_FOR_GET_CHANNEL_ADVICE',
    default=(
        'На основе информации о пользователе предложи наилучший ' +
        'банковский продукт'
    ),
)