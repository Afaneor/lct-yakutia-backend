import rules
from rules.predicates import is_authenticated

view_sale_channel = is_authenticated
list_sale_channel = is_authenticated


def has_view_sale_channel(user, sale_channel):
    """Права на просмотр каналов продаж."""
    return view_sale_channel(user, sale_channel)


def has_list_sale_channel(user, sale_channel):
    """Права на просмотр списка каналов продаж."""
    return list_sale_channel(user, sale_channel)


rules.set_perm('g_mtg.view_salechannel', has_view_sale_channel)
rules.set_perm('g_mtg.list_salechannel', has_list_sale_channel)
