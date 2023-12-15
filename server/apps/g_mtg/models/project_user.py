from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel
from server.apps.services.enums import UserRoleInProject


class ProjectUser(AbstractBaseModel):
    """Пользователь проекта."""

    project = models.ForeignKey(
        to='g_mtg.Project',
        on_delete=models.CASCADE,
        verbose_name=_('Продукт банка'),
        related_name='projects_users',
        db_index=True,
    )
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='projects_users',
        db_index=True,
    )
    role = models.CharField(
        verbose_name=_('Роль в проекте'),
        choices=UserRoleInProject.choices,
        default=UserRoleInProject.PERFORMER,
        max_length=settings.MAX_STRING_LENGTH,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Пользователь, участвующий в проекте')
        verbose_name_plural = _('Пользователи, участвующие в проектах')
        constraints = [
            models.UniqueConstraint(
                fields=('project', 'user'),
                name='unique_user_for_project',
            ),
            models.CheckConstraint(
                name='project_user_role_valid',
                check=models.Q(role__in=UserRoleInProject.values),
            ),
        ]

    def __str__(self):
        return f'{self.project} - {self.user}'
