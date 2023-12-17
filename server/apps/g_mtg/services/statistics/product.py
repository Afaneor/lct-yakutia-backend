from typing import Any, Dict, List

from django.db import models
from django.db.models import QuerySet

from server.apps.g_mtg.models import Product, Project, ProjectSaleChannel
from server.apps.llm_request.models import RequestData


def get_statistics_for_product(
    queryset: QuerySet[Product],
    projects_id: List[str],
) -> Dict[str, Any]:
    """Получение статистики для продукта."""
    products_id = queryset.values_list('id', flat=True)

    if projects_id:
        return {
            'project_sale_channel': {
                'name': 'Статистика по канала продаж',
                'data': [
                    {
                        'type': 'die',
                        'name': 'Количество каналов продаж для продукта',
                        'value': ProjectSaleChannel.objects.filter(
                            project__in=projects_id,
                        ).count()
                    },
                ],
            },
            'request_data': {
                'name': 'Статистика по запросам пользователей',
                'data': [
                    {
                        'type': 'circular',
                        'name': 'Количество запросов в модель в рамках проекта по статусам',
                        'value': RequestData.objects.filter(
                            project_sale_channel__project__in=projects_id,
                        ).values(
                            'status',
                        ).annotate(
                            count=models.Count('id'),
                        ).order_by('-count'),
                    },
                    {
                        'type': 'circular',
                        'name': 'Количество запросов в модель в рамках проекта по успешности',
                        'value': RequestData.objects.filter(
                            project_sale_channel__project__in=projects_id,
                        ).values(
                            'success_type',
                        ).annotate(
                            count=models.Count('id'),
                        ).order_by('-count'),
                    },
                ],
            },
        }

    return {
        'projects': {
            'name': 'Статистика по проектам',
            'data': [
                {
                    'type': 'circular',
                    'name': 'Количество проектов для продукта',
                    'value': Project.objects.filter(
                        product__in=products_id,
                    ).values(
                        name=models.F('product__name'),
                    ).annotate(
                        count=models.Count('id'),
                    ).order_by('-count'),
                },
            ],
        },
        'project_sale_channel': {
            'name': 'Статистика по канала продаж',
            'data': [
                {
                    'type': 'columnar',
                    'name': 'Количество проектов по каналам продаж',
                    'value': ProjectSaleChannel.objects.filter(
                        project__product__in=products_id,
                    ).values(
                        name=models.F('sale_channel__name'),
                    ).annotate(
                        count=models.Count('id'),
                    ).order_by('-count'),
                },
            ],
        },
        'request_data': {
            'name': 'Статистика по запросам пользователей',
            'data': [
                {
                    'type': 'circular',
                    'name': 'Количество запросов в модель в рамках продукта по статусам',
                    'value': RequestData.objects.filter(
                        project_sale_channel__project__product__in=products_id,
                    ).values(
                        'status',
                    ).annotate(
                        count=models.Count('id'),
                    ).order_by('-count'),
                },
                {
                    'type': 'circular',
                    'name': 'Количество запросов в модель в рамках продукта по успешности',
                    'value': RequestData.objects.filter(
                        project_sale_channel__project__product__in=products_id,
                    ).values(
                        'success_type',
                    ).annotate(
                        count=models.Count('id'),
                    ).order_by('-count'),
                },
            ],
        },
    }
