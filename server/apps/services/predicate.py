from rules import predicate

from server.apps.services.enums import UserRoleInProject
from server.apps.user.models import User


@predicate  # type: ignore
def is_manager(user: User) -> bool:
    """Проверка роли пользователя. Менеджер проекта."""
    user_role = user.role
    if isinstance(user_role, dict):
        return UserRoleInProject.MANAGER in user_role.values()  # type: ignore
    return False


def manager_within_project(user: User, project_id: int) -> bool:
    """Проверка, что пользователь в рамках проекта является менеджером.."""
    user_role = user.role
    if isinstance(user_role, dict):
        return user_role.get(project_id) == UserRoleInProject.MANAGER
    return False
