from django.contrib import admin

from .models import Client, Mailing, Message, Operator, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ["code", "name"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "operator_code",
        "timezone",
    )
    list_filter = ["operator_code"]
    search_fields = ["phone_number"]
    # inlines = (TagInline,)
    fieldsets = [
        (None, {"fields": ["phone_number", "operator_code", "timezone", "tags"]}),
    ]


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "text",
        "start_datetime",
        "end_datetime",
    )
    list_filter = ["start_datetime"]
    search_fields = ["text", "title"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "text",
                    "start_datetime",
                    "end_datetime",
                    "tags",
                    "operators",
                ]
            },
        ),
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "create_datetime",
        "status",
        "mailing",
        "client",
    )
    list_filter = ["status"]
    readonly_fields = ["create_datetime", "status", "mailing", "client"]
