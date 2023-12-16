from typing import Any, Dict, List

from django.db import models
from django.db.models import QuerySet

from server.apps.g_mtg.models import Project, ProjectSaleChannel, ProjectUser
from server.apps.services.enums import SuccessType, UserRoleInProject
from server.apps.user.models import User
from server.apps.user_request.models import UserRequest


def create_project(
    validated_data: Dict[str, Any],
    user: User,
) -> Project:
    """Добавление проекта и пользователя к нему."""
    project = Project.objects.create(**validated_data)
    ProjectUser.objects.create(
        project=project,
        user=user,
        role=UserRoleInProject.MANAGER,
    )

    return project


def create_project_sale_channel(
    validated_data: Dict[str, Any],
) -> None:
    """Создание в проекте каналов связи."""
    ProjectSaleChannel.objects.bulk_create(
        [
            ProjectSaleChannel(
                project=validated_data['project'],
                sale_channel=sale_channel,
            )
            for sale_channel in validated_data['sales_channels']
        ]
    )


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
                        'value': UserRequest.objects.filter(
                            project_sale_channel__project__in=projects_id,
                        ).values(
                            product=models.F('project_sale_channel__project__product'),
                        ).annotate(count=models.Count('id')).order_by('-count'),
                    },
                    {
                        'type': 'круговая',
                        'name': 'Стата по типу успешности в рамка продукта',
                        'value': UserRequest.objects.filter(
                            project_sale_channel__project__in=projects_id,
                            success_type__in={SuccessType.SOLD, SuccessType.INTEREST},
                        ).values(
                            'project_sale_channel__project__product'
                        ).annotate(count=models.Count('id')).order_by('-count'),
                    },
                ],
            },
            'user_request': {
                'name': 'Статистика по запросам',
                'data': [
                    {
                        'type': 'круговая',
                        'name': 'Стата по успешности запросов в проектах',
                        'value': UserRequest.objects.filter(
                            project_sale_channel__project__in=projects_id,
                        ).values(
                            'success_type',
                        ).annotate(count=models.Count('id')).order_by('-count'),
                    },
                ],
            },
        }

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
                    'value': UserRequest.objects.filter(
                        project_sale_channel__project__in=projects_id,
                        success_type__in={SuccessType.SOLD, SuccessType.INTEREST},
                    ).values(
                        'project_sale_channel__project__product'
                    ).annotate(count=models.Count('id')).order_by('-count'),
                },
            ],
        },
        'user_request': {
            'name': 'Статистика по запросам',
            'data': [
                {
                    'type': 'круговая',
                    'name': 'Стата по успешности запросов в проектах',
                    'value': UserRequest.objects.filter(
                        project_sale_channel__project__in=projects_id,
                    ).values(
                        'success_type',
                    ).annotate(count=models.Count('id')).order_by('-count'),
                },
            ],
        },
    }

