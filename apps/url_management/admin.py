from django.contrib import admin
from apps.url_management.models import RedirectRule


@admin.register(RedirectRule)
class RedirectRuleAdmin(admin.ModelAdmin):
    list_display = ("redirect_identifier", "redirect_url", "is_private", "owner", "created", "modified")
    list_filter = ("is_private", "owner", "created")
    search_fields = ("redirect_identifier", "redirect_url", "owner__username")
    readonly_fields = ("id", "created", "modified", "redirect_identifier", "owner")

    ordering = ("-created",)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.owner == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.owner == request.user
        return True
