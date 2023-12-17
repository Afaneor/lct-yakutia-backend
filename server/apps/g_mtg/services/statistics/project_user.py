from typing import Any, Dict

from django.db import models
from django.db.models import QuerySet

from server.apps.g_mtg.models import ProjectUser
from server.apps.llm_request.models import MarketingTextRequest
from server.apps.services.enums import SuccessType, UserRoleInProject


def get_project_user_statistics(
    queryset: QuerySet[ProjectUser],
) -> Dict[str, Any]:
    """Получение общей статистики по проекту.

    1) user_request_count - количество запросов по каждому пользователю.
    2) user_request_sold - количество проданных продуктов по каждому
    пользователю.
    """
    marketing_text_request = MarketingTextRequest.objects.filter(
        user__in=queryset.values('user')
    )

    return {
        'user_request_count': marketing_text_request.values(
            'user'
        ).annotate(count=models.Count('id')).order_by('-count'),
        'user_request_sold': marketing_text_request.filter(
            success_type=SuccessType.SOLD,
        ).values(
            'user'
        ).annotate(count=models.Count('id')).order_by('-count'),
    }
