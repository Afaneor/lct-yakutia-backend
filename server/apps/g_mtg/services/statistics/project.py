from typing import Any, Dict, List

from django.db.models import QuerySet

from server.apps.g_mtg.models import Project, ProjectUser
from server.apps.llm_request.models import MarketingTextRequest
from server.apps.services.enums import SuccessType


def get_statistics(
    projects_id: List[str],
    queryset: QuerySet[Project],
) -> Dict[str, Any]:
    """Формирование статистики по проекту."""
    if not projects_id:
        projects_id = queryset.values_list('id', flat=True)

    if len(projects_id) > 1:
        return {
            'user_count': {
                'name': 'Количество пользователей',
                'data': ProjectUser.objects.filter(
                    project__in=projects_id,
                ).count(),
            },
            'products': {
                'name': 'Статистика по продуктам',
                'data': [
                    {
                        'type': 'круговая',
                        'name': 'Стата по продуктам в проектах',
                        'value': MarketingTextRequest.objects.filter(
                            project_sale_channel__project__in=projects_id,
                        ).values(
                            product=models.F('project_sale_channel__project__product'),
                        ).annotate(count=models.Count('id')).order_by('-count'),
                    },
                    {
                        'type': 'круговая',
                        'name': 'Стата по типу успешности в рамка продукта',
                        'value': MarketingTextRequest.objects.filter(
                            project_sale_channel__project__in=projects_id,
                            success_type__in={SuccessType.SOLD, SuccessType.INTEREST},
                        ).values(
                            'project_sale_channel__project__product'
                        ).annotate(count=models.Count('id')).order_by('-count'),
                    },
                ],
            },
            'marketing_text_request': {
                'name': 'Статистика по запросам',
                'data': [
                    {
                        'type': 'круговая',
                        'name': 'Стата по успешности запросов в проектах',
                        'value': MarketingTextRequest.objects.filter(
                            project_sale_channel__project__in=projects_id,
                        ).values(
                            'success_type',
                        ).annotate(count=models.Count('id')).order_by('-count'),
                    },
                ],
            },
        }

    from django.db import models
    return {
        'user_count': {
            'name': 'Количество пользователей',
            'data': ProjectUser.objects.filter(
                project__in=projects_id,
            ).count(),
        },
        'products': {
            'name': 'Статистика по продуктам',
            'data': [
                {
                    'type': 'круговая',
                    'name': 'Стата по типу успешности в рамка продукта',
                    'value': MarketingTextRequest.objects.filter(
                        project_sale_channel__project__in=projects_id,
                        success_type__in={SuccessType.SOLD, SuccessType.INTEREST},
                    ).values(
                        'project_sale_channel__project__product'
                    ).annotate(count=models.Count('id')).order_by('-count'),
                },
            ],
        },
        'marketing_text_request': {
            'name': 'Статистика по запросам',
            'data': [
                {
                    'type': 'круговая',
                    'name': 'Стата по успешности запросов в проектах',
                    'value': MarketingTextRequest.objects.filter(
                        project_sale_channel__project__in=projects_id,
                    ).values(
                        'success_type',
                    ).annotate(count=models.Count('id')).order_by('-count'),
                },
            ],
        },
    }

