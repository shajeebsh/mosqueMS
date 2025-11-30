from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


class MosqueProfilePage(Page):
    parent_page_types = ["wagtailcore.Page"]  # only one allowed
    subpage_types = []
    max_count = 1


mosque_name = models.CharField(max_length=120)
tagline = models.CharField(max_length=180, blank=True)
logo = models.ForeignKey(
    "wagtailimages.Image",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="+",
)
cover_image = models.ForeignKey(
    "wagtailimages.Image",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="+",
)
address = models.TextField()
phone = models.CharField(max_length=20, blank=True)
email = models.EmailField(blank=True)
website = models.URLField(blank=True)
bank_details = models.TextField(
    help_text="One per line:  Bank | Branch | A/C No | IFSC",
    blank=True,
)
facebook = models.URLField(blank=True)
twitter = models.URLField(blank=True)
instagram = models.URLField(blank=True)
youtube = models.URLField(blank=True)

content_panels = Page.content_panels + [
    MultiFieldPanel(
        [
            FieldPanel("mosque_name"),
            FieldPanel("tagline"),
            FieldPanel("logo"),
            FieldPanel("cover_image"),
        ],
        heading="Branding",
    ),
    MultiFieldPanel(
        [
            FieldPanel("address"),
            FieldPanel("phone"),
            FieldPanel("email"),
            FieldPanel("website"),
        ],
        heading="Contact",
    ),
    FieldPanel("bank_details"),
    MultiFieldPanel(
        [
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),
        ],
        heading="Social Links",
    ),
]


class Meta:
    verbose_name = "Mosque Profile"


@register_setting
class CoreSettings(BaseSiteSetting):
    prayer_times_footer = models.BooleanField(
        default=True,
        help_text="Show prayer times in site footer",
    )


holidays_page = models.ForeignKey(
    "wagtailcore.Page",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    help_text="Page that displays holiday list",
)
panels = [
    FieldPanel("prayer_times_footer"),
    FieldPanel("holidays_page"),
]
