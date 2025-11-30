from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from django.conf import settings

@hooks.register("construct_main_menu")
def add_members_menu(request, menu_items):
    if not getattr(settings, "ENABLE_MEMBERS_MODULE", False):
        return
    from wagtail.admin.menu import MenuItem
    menu_items.append(
        MenuItem("Members", reverse("wagtailadmin_explore_root") + "members/", icon_name="group", order=200)
    )