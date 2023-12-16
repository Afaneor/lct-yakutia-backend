import rules
from rules.predicates import is_authenticated

from server.apps.services.predicate import is_manager, manager_within_project


@rules.predicate
def is_owned_by_project(user, project_user):
    """Просмотр пользователей."""
    return project_user.project in user.projects.all()


@rules.predicate
def is_manager_within_project(user, project_user):
    """Удалять сотрудника проекта можно менеджерам."""
    if user != project_user.user:
        return manager_within_project(
            user=user,
            project_id=project_user.project.id,
        )
    return False


view_project_user = is_owned_by_project
add_project_user = is_manager
statistics_project_user = is_manager
delete_project_user = is_manager_within_project


def has_view_project_user(user, project_user):
    """Права на просмотр пользователей проекта."""
    return view_project_user(user, project_user)


def has_add_project_user(user):
    """Права на добавление пользователя в проект."""
    return add_project_user(user)


def has_delete_project_user(user, project_user):
    """Права на удаление пользователя."""
    return delete_project_user(user, project_user)


def has_statistics_project_user(user):
    """Права на просмотр статистики."""
    return statistics_project_user(user)


rules.set_perm('g_mtg.view_projectuser', has_view_project_user)
rules.set_perm('g_mtg.add_projectuser', has_add_project_user)
rules.set_perm('g_mtg.delete_projectuser', has_delete_project_user)
rules.set_perm('g_mtg.statistics_projectuser', has_statistics_project_user)
rules.set_perm('g_mtg.list_projectuser', is_authenticated)
