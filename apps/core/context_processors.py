from django.conf import settings
from django.utils import timezone
from .snippets import PrayerTime, Holiday


def mosque(request):
    from .models import MosqueProfilePage

    if not settings.ENABLE_CORE_MODULE:
        return {"mosque": None}

    mosque_page = MosqueProfilePage.objects.first()
    return {"mosque": mosque_page}


def prayer_holidays(request):
    if not settings.ENABLE_CORE_MODULE:
        return {}
    return {
        "prayer_times": PrayerTime.objects.all(),
        "holidays": Holiday.objects.filter(date__gte=timezone.now().date())[:10],
    }
