# admin_custom/context_processors.py
from .menu_list import APP_MENUS


def admin_menu(request):
    print("admin_menu context processor called")
    return {'APP_MENUS': APP_MENUS}