from django.conf import settings
from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
        
class Icon(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        CHANGES_REQUESTED = "changes_requested", "Changes Requested"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PUBLISHED = "published", "Published"

    unique_id = models.CharField(max_length=100, unique=True)
    designer = models.CharField(max_length=200, blank=True)
    metadata_source = models.CharField(max_length=200, blank=True)
    uploader = models.CharField(max_length=200, blank=True)

    primary_tag = models.CharField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="icons")  # from secondary-tags

    when_created = models.CharField(max_length=50, blank=True)   # text for now; dates in CSV are messy
    when_uploaded = models.CharField(max_length=50, blank=True)
    where_created = models.CharField(max_length=200, blank=True)
    icon_geography = models.CharField(max_length=200, blank=True)

    icon_description = models.TextField(blank=True)
    icon_context = models.TextField(blank=True)
    creation_context = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.PENDING,
    )

    png_file = models.FileField(upload_to="icons/png/", blank=True, null=True)
    svg_file = models.FileField(upload_to="icons/svg/", blank=True, null=True)

    # Who uploaded this icon. Null for rows loaded by import_icons (they predate
    # accounts), so those are moderator-only to edit: there is no owner to match.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="icons",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.primary_tag or self.unique_id
