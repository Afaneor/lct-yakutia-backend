import rules
from rules.predicates import is_authenticated

from server.apps.services.predicate import is_manager, manager_within_project


@rules.predicate
def is_owned_by_project(user, project):
    """Просмотр проекта."""
    return project in user.projects.all()


@rules.predicate
def is_manager_within_project(user, project):
    """Редактировать проект может менеджер внутри проекта."""
    if user in project.users.all():
        return manager_within_project(
            user=user,
            project_id=project.id,
        )
    return False


view_project = is_owned_by_project
add_project = is_authenticated
change_project = is_manager
# statistics_project = is_manager


def has_view_project(user, project):
    """Права на просмотр проекта."""
    return view_project(user, project)


def has_add_project(user):
    """Права на добавление проекта."""
    return add_project(user)


def has_change_project(user, project):
    """Права на редактирование проекта."""
    return change_project(user, project)


# def has_statistics_project(user):
#     """Права на просмотр статистики."""
#     return statistics_project(user)


rules.set_perm('g_mtg.view_project', has_view_project)
rules.set_perm('g_mtg.add_project', has_add_project)
rules.set_perm('g_mtg.change_project', has_change_project)
# rules.set_perm('g_mtg.statistics_project', has_statistics_project)
rules.set_perm('g_mtg.list_project', is_authenticated)
