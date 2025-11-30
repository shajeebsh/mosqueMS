from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class PrayerTime(models.Model):
    DAY_CHOICES = [
        (i, n)
        for i, n in enumerate(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
    ]
    day = models.IntegerField(choices=DAY_CHOICES, unique=True)
    fajr = models.TimeField()
    sunrise = models.TimeField()
    dhuhr = models.TimeField()
    asr = models.TimeField()
    maghrib = models.TimeField()
    isha = models.TimeField()
    jumuah = models.TimeField(null=True, blank=True, help_text="Only for Friday")
    panels = [
        FieldPanel("day"),
        FieldPanel("fajr"),
        FieldPanel("sunrise"),
        FieldPanel("dhuhr"),
        FieldPanel("asr"),
        FieldPanel("maghrib"),
        FieldPanel("isha"),
        FieldPanel("jumuah"),
    ]


def __str__(self):
    return self.get_day_display()


class Meta:
    ordering = ["day"]


@register_snippet
class Holiday(models.Model):
    name = models.CharField(max_length=80)
    date = models.DateField()
    note = models.TextField(blank=True)


panels = [
    FieldPanel("name"),
    FieldPanel("date"),
    FieldPanel("note"),
]


def __str__(self):
    return f"{self.name} ({self.date})"


class Meta:
    ordering = ["date"]
