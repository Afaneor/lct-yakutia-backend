import rules
from rules.predicates import is_authenticated

view_product = is_authenticated
list_product = is_authenticated


def has_view_product(user, product):
    """Права на просмотр продукта."""
    return view_product(user, product)


def has_list_product(user, product):
    """Права на просмотр списка продуктов."""
    return list_product(user, product)


rules.set_perm('g_mtg.view_product', has_view_product)
rules.set_perm('g_mtg.list_product', has_list_product)
