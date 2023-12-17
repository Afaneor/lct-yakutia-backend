

class SendException(Exception):  # noqa: N818
    """Сервис с llm_model не доступен."""


class ApiException(Exception):  # noqa: N818
    """Некорректная отправка данных в llm_model."""