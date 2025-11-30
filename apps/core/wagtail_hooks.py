from wagtail import hooks
from django.urls import reverse
from django.conf import settings
from .models import MosqueProfilePage


@hooks.register("construct_main_menu")
def add_mosque_profile_item(request, menu_items):
    if not settings.ENABLE_CORE_MODULE:
        return
    page = MosqueProfilePage.objects.first()
    if not page:
        return
    from wagtail.admin.menu import MenuItem
    menu_items.append(
        MenuItem(
            "Mosque Profile",
            reverse("wagtailadmin_pages:edit", args=[page.id]),
            icon_name="place",
            order=100,
        )
    )