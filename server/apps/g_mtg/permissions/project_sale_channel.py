import rules
from rules.predicates import is_authenticated

from server.apps.services.predicate import is_manager, manager_within_project


@rules.predicate
def is_owned_by_project(user, project_sale_channel):
    """Просмотр проекта."""
    return project_sale_channel.project in user.projects.all()


@rules.predicate
def is_manager_within_project(user, project):
    """Редактировать проект может менеджер внутри проекта."""
    if user in project.users.all():
        return manager_within_project(
            user=user,
            project_id=project.id,
        )
    return False


view_project_sale_channel = is_owned_by_project
add_client_project_sale_channel = is_authenticated
add_channel_project_sale_channel = is_authenticated
statistics_project_sale_channel = is_manager


def has_view_project_sale_channel(user, project_sale_channel):
    """Права на просмотр каналов проекта."""
    return view_project_sale_channel(user, project_sale_channel)


def has_add_client_project_sale_channel(user):
    """Права на добавление пользователей."""
    return add_client_project_sale_channel(user)


def has_add_channel_project_sale_channel(user):
    """Права на добавление каналов."""
    return add_channel_project_sale_channel(user)


def has_statistics_project_sale_channel(user):
    """Права на просмотр статистики."""
    return statistics_project_sale_channel(user)


rules.set_perm(
    'g_mtg.view_projectsalechannel',
    has_view_project_sale_channel,
)
rules.set_perm(
    'g_mtg.add_client_projectsalechannel',
    has_add_client_project_sale_channel,
)
rules.set_perm(
    'g_mtg.add_channel_projectsalechannel',
    has_add_channel_project_sale_channel,
)
rules.set_perm(
    'g_mtg.statistics_projectsalechannel',
    has_statistics_project_sale_channel,
)
rules.set_perm(
    'g_mtg.list_projectsalechannel',
    is_authenticated,
)
