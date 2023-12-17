from django.db import models
from django.utils.translation import gettext_lazy as _


class ClientType(models.TextChoices):
    """Тип клиента."""

    SUPER_WAGES = 'super_wages', _('Супер-ЗП')
    MASS_WAGES_CREDITED = 'mass_wages_credited', _('Масс-ЗП закредитованные')
    MASS_WAGES_WITHOUT_BCI = 'mass_wages_without_bci', _('Масс-ЗП без согласия БКИ')
    FORMER_SALARY_EARNERS = 'former_salary_earners', _('Бывшие зарплатники')
    DEPOSITS_IN_OUTFLOW = 'deposits_in_outflow', _('Депозиты в оттоке')
    CURRENT_BORROWERS = 'current_borrowers', _('Текущие заемщики')
    SUPER_AFFLUENT = 'super_affluent', _('Текущие заемщики')
    DC_WK_UP_TO_6_MOBS = 'dc_wk_up_to_6_mobs', _('ДК/ЗК до 6 моба')
    SUPER_DEPOSITS = 'super_deposits', _('Супер-депозиты')
    FORMER_BORROWERS = 'Former borrowers', _('Бывшие заемщики')


class RequestStatus(models.TextChoices):
    """Статус запроса."""

    OK = 'ok', _('Ок')
    ERROR = 'error', _('Ошибка')
    INITIAL = 'initial', _('Исходный')
    IN_PROGRESS = 'in_progress', _('В процессе')


class MessageStatus(models.TextChoices):
    """Статус сообщения."""

    OK = 'ok', _('Данные сформированы хорошо')
    ERROR = 'error', _('Ошибка при формировании данных')
    REVISION = 'revision', _('Доработка сформированных данных')
    UNDEFINED = 'undefined', _('Не определено')


class MessageType(models.TextChoices):
    """Тип сообщения."""

    USER = 'user', _('Пользовательское')
    SYSTEM = 'system', _('Системное')


class SuccessType(models.TextChoices):
    """Тип успеха."""

    SOLD = 'sold', _('Продано')
    REFLECTION = 'reflection', _('Обдумывание')
    INTEREST = 'interest', _('Заинтересованность')
    NEGATIVE_REACTION = 'negative_reaction', _('Негативная реакция')
    POSITIVE_REACTION = 'positive_reaction', _('Позитивная реакция')
    UNDEFINED = 'undefined', _('Не определено')


class UserRoleInProject(models.TextChoices):
    """Роль пользователя."""

    MANAGER = 'manager', _('Руководитель')
    PERFORMER = 'performer', _('Исполнитель')
