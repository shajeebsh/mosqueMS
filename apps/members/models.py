from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from django.contrib.auth.models import User
import qrcode, io
from django.core.files import File
from django.urls import reverse


class Family(Page):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []  # ["members.Member"] or ["members.MemberDetailPage"] once you create one
    max_count = None

    head_of_family = models.ForeignKey(
        "members.Member", null=True, blank=True, on_delete=models.SET_NULL, related_name="headed_families"
    )
    spouse = models.ForeignKey(
        "members.Member", null=True, blank=True, on_delete=models.SET_NULL, related_name="spouse_families"
    )
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    qr_code = models.ImageField(upload_to="qr/", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("head_of_family"),
        FieldPanel("spouse"),
        FieldPanel("address"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("qr_code"),
    ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr()

    def generate_qr(self):
        url = reverse("wagtailadmin_pages:edit", args=[self.id])
        img = qrcode.make(f"https://yourdomain.com{url}")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        file_name = f"family_{self.id}.png"
        self.qr_code.save(file_name, File(buf), save=False)
        super().save(update_fields=["qr_code"])

    class Meta:
        verbose_name = "Family"


class Member(models.Model):
    RELATION_CHOICES = [
        ("self", "Self"),
        ("spouse", "Spouse"),
        ("child", "Child"),
        ("parent", "Parent"),
    ]
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="members")
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES, default="self")
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_alive = models.BooleanField(default=True)

    panels = [
        FieldPanel("user"),
        FieldPanel("name"),
        FieldPanel("relation"),
        FieldPanel("gender"),
        FieldPanel("date_of_birth"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("is_alive"),
    ]

    def __str__(self):
        return f"{self.name} ({self.relation})"


@register_snippet
class VitalEvent(models.Model):
    EVENT_CHOICES = [("birth", "Birth"), ("marriage", "Marriage"), ("death", "Death")]
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    person = models.CharField(max_length=100)  # name of person
    date = models.DateField()
    note = models.TextField(blank=True)
    document = models.FileField(upload_to="vitals/%Y/%m/", blank=True)

    panels = [
        FieldPanel("family"),
        FieldPanel("event_type"),
        FieldPanel("person"),
        FieldPanel("date"),
        FieldPanel("note"),
        FieldPanel("document"),
    ]

    def __str__(self):
        return f"{self.get_event_type_display()} – {self.person} ({self.date})"

    class Meta:
        ordering = ["-date"]