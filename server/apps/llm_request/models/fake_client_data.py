from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class FakeClientData(AbstractBaseModel):

    gender = models.CharField(
        verbose_name=_('Пол клиента (0 муж, 1 жен)'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    age = models.CharField(
        verbose_name=_('Возраст Клиента'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    reg_region_nm = models.CharField(
        verbose_name=_('Регион'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_all_3m = models.CharField(
        verbose_name=_('Количество транзакций за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_top_up_3m = models.CharField(
        verbose_name=_('Количество приходных операций за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_cash_3m = models.CharField(
        verbose_name=_('Количество операций выдачи наличных за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_buy_3m = models.CharField(
        verbose_name=_('Количество операций оплаты покупок за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_mobile_3m = models.CharField(
        verbose_name=_('Количество операций оплаты связи за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_oil_3m = models.CharField(
        verbose_name=_('Количество операций оплаты на АЗС за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_on_card_3m = models.CharField(
        verbose_name=_('Количество операций переводов по карте за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_tr_service_3m = models.CharField(
        verbose_name=_('Количество операций оплаты услуг за последние 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_zp_12m = models.CharField(
        verbose_name=_('Количество зарплатных поступлений за 12 месяцев'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    sum_zp_12m = models.CharField(
        verbose_name=_('Сумма зарплатных поступлений за 12m'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    limit_exchange_count = models.CharField(
        verbose_name=_('Общее количество изменений лимита'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    max_outstanding_amount_6m = models.CharField(
        verbose_name=_('Максимальная задолженность по основному долгу за 6 месяцев'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    avg_outstanding_amount_3m = models.CharField(
        verbose_name=_('Средняя задолженность по основному долгу за 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    cnt_dep_act = models.CharField(
        verbose_name=_('Количество активных срочных депозитов, имеющих текущий остаток более 1000 р'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    sum_dep_now = models.CharField(
        verbose_name=_('Текущая общая сумма (в рублях) срочных депозитов'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    avg_dep_avg_balance_1month = models.CharField(
        verbose_name=_('Средний баланс по всем депозитам за последний месяц'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    max_dep_avg_balance_3month = models.CharField(
        verbose_name=_('Максимальный баланс по всем депозитам за 3 месяца'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    app_vehicle_ind = models.CharField(
        verbose_name=_('Наличие авто'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    app_position_type_nm = models.CharField(
        verbose_name=_('Уровень занимаемой позиции'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    visit_purposes = models.CharField(
        verbose_name=_('Цель последнего посещения офиса'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    qnt_months_from_last_visit = models.CharField(
        verbose_name=_('Количество месяцев с прошлого посещения офиса'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    super_clust = models.CharField(
        verbose_name=_('Кластер клиента'),
        max_length=settings.MAX_STRING_LENGTH,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _(
            'Данные клиентов для тестирования загрузки данных из postgres',
        )
        verbose_name_plural = _(
            'Данные клиентов для тестирования загрузки данных из postgres',
        )

    def __str__(self):
        return f'Возраст: {self.age}. Пол: {self.gender}'
