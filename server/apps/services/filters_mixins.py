from typing import List, Optional

import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_filters.fields import MultipleChoiceField


class NonValidatingMultipleChoiceField(MultipleChoiceField):
    """Поле для множественного выбора данных без валидации."""

    def validate(self, value):  # noqa: WPS110
        """Отключение валидации, чтобы можно было передавать любые значения."""
        pass  # noqa: WPS420


class NonValidatingMultipleChoiceFilter(django_filters.MultipleChoiceFilter):
    """Фильтр для множественного выбора данных без валидации."""

    field_class = NonValidatingMultipleChoiceField


class CreatedUpdatedDateFilterMixin(django_filters.FilterSet):
    """Миксин для фильтрации по датам создания и обновления."""

    created_at_date = django_filters.DateFromToRangeFilter(
        field_name='created_at__date',
        label=_(
            'Поиск по дате создания. Суффикс "_after" означает GTE поиск.' +
            'Суффикс "_before" означает LTE поиск. ' +
            'Можно указывать created_at_date_after и created_at_date_before ' +
            'как вместе, так и по раздельности',
        ),
    )

    updated_at_date = django_filters.DateFromToRangeFilter(
        field_name='updated_at__date',
        label=_(
            'Поиск по дате создания. Суффикс "_after" означает GTE поиск.' +
            'Суффикс "_before" означает LTE поиск. ' +
            'Можно указывать created_at_date_after и created_at_date_before ' +
            'как вместе, так и по раздельности',
        ),
    )


class UserFilterMixin(django_filters.FilterSet):
    """Миксин для фильтрации по пользователю."""

    user = django_filters.AllValuesMultipleFilter(
        field_name='user',
        label=_('Поиск по пользователю'),
    )
    user_email = django_filters.AllValuesMultipleFilter(
        field_name='user__email',
        label=_('Поиск по email пользователя'),
    )
    user_username = django_filters.AllValuesMultipleFilter(
        field_name='user_username',
        label=_('Поиск по username пользователя'),
    )
    user_first_name = django_filters.AllValuesMultipleFilter(
        field_name='user__first_name',
        label=_('Поиск по указанному шаблону в имени пользователя'),
    )
    user_last_name = django_filters.AllValuesMultipleFilter(
        field_name='user__last_name',
        label=_('Поиск по указанному шаблону в фамилии пользователя'),
    )
