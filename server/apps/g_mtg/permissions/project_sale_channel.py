import rules
from rules.predicates import is_authenticated


@rules.predicate
def is_owned_by_project(user, project_sale_channel):
    """Просмотр проекта."""
    return project_sale_channel.project in user.projects.all()


view_project_sale_channel = is_owned_by_project
add_client_project_sale_channel = is_authenticated
add_channel_project_sale_channel = is_authenticated
change_project_sale_channel = is_owned_by_project
list_project_sale_channel = is_authenticated


def has_view_project_sale_channel(user, project_sale_channel):
    """Права на просмотр каналов проекта."""
    return view_project_sale_channel(user, project_sale_channel)


def has_add_client_project_sale_channel(user):
    """Права на добавление каналов в проект."""
    return add_client_project_sale_channel(user)


def has_add_channel_project_sale_channel(user):
    """Права на добавление каналов в проекте."""
    return add_channel_project_sale_channel(user)


def has_change_project_sale_channel(user, project_sale_channel):
    """Права на изменение канала в проекте."""
    return change_project_sale_channel(user, project_sale_channel)


def has_list_project_sale_channel(user, project_sale_channel):
    """Права на просмотр списка каналов в проекте."""
    return list_project_sale_channel(user, project_sale_channel)


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
    'g_mtg.change_channel_projectsalechannel',
    has_change_project_sale_channel,
)
rules.set_perm(
    'g_mtg.list_projectsalechannel',
    has_list_project_sale_channel,
)
