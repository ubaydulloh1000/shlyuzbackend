from django.contrib import admin

from . import models


@admin.register(models.Chat)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "owner", "created_at", "updated_at")
    list_display_links = ("id", "name")
    search_fields = ("name", "owner__username",)
    list_filter = ("type", "owner",)


@admin.register(models.ChatMembership)
class ChatMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "user", "created_at", "updated_at")
    list_display_links = ("id", "chat")
    search_fields = ("chat__name", "user__username",)
    autocomplete_fields = ("chat", "user",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "sender", "type",
                    "short_content", "created_at")
    list_display_links = ("id", "chat")
    search_fields = ("chat__name", "sender__username", "content")
    list_filter = ("chat", "sender", "type",)

    def short_content(self, obj):
        return obj.content[:40]
