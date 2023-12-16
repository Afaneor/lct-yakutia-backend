import rules
from rules.predicates import is_authenticated

from server.apps.services.predicate import is_manager

view_product = is_authenticated
statistics_product = is_manager


def has_view_product(user, product):
    """Права на просмотр продукта."""
    return view_product(user, product)


rules.set_perm('g_mtg.view_product', has_view_product)
rules.set_perm('g_mtg.list_product', is_authenticated)
