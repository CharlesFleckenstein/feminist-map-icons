from django.contrib import admin
from .models import Icon, Tag
from .roles import is_admin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ("unique_id", "primary_tag", "designer", "status", "created_by", "updated_at")
    list_filter = ("status",)
    search_fields = ("unique_id", "primary_tag", "designer", "uploader", "icon_description")
    filter_horizontal = ("tags",)

    # The admin is a second way in, and it does not go through the API's permission
    # classes. Moderators are given is_staff to review here, and the role groups give them
    # change_icon, so without this the status dropdown let them publish directly and
    # "approve is not publish" held only on the API. created_by is locked for the same
    # reason: the form would otherwise let them reassign authorship.
    RESERVED_TO_ADMINS = ("status", "created_by")

    def get_readonly_fields(self, request, obj=None):
        if is_admin(request.user):
            return super().get_readonly_fields(request, obj)
        return tuple(super().get_readonly_fields(request, obj)) + self.RESERVED_TO_ADMINS

    # A readonly field is simply absent from the add form, so a non-admin creating an icon
    # here would silently get the model default (pending). That is the right state, but be
    # explicit rather than relying on it.
    def save_model(self, request, obj, form, change):
        if not change and not is_admin(request.user):
            obj.status = Icon.Status.PENDING
        super().save_model(request, obj, form, change)
