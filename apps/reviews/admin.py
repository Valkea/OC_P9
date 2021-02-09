from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Ticket, Review

# admin.site.register(Ticket)
# admin.site.register(Review)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "ticket_photo",
    )

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "description",
                    "user",
                    "image",
                    "ticket_photo",
                ]
            },
        ),
    ]

    readonly_fields = ["user", "ticket_photo"]

    def ticket_photo(self, obj):
        return mark_safe(
            '<img src="{}" title="{}" height="300px"/>'.format(obj.image.url, obj.title)
        )

    ticket_photo.admin_order_field = "image"  # Allows column order sorting
    ticket_photo.short_description = "Vignette"  # Renames column head

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "headline",
        "get_ticket",
        "ticket_photo",
    )

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "headline",
                    "body",
                    "user",
                    "get_ticket",
                    "ticket_photo",
                ]
            },
        ),
    ]

    readonly_fields = ["user", "get_ticket", "ticket_photo"]

    def get_ticket(self, obj):
        # return obj.ticket.title
        path = "admin:reviews_ticket_change"
        url = reverse(path, args=(obj.ticket.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.ticket.title))

    get_ticket.admin_order_field = "ticket"  # Allows column order sorting
    get_ticket.short_description = "Ticket associé"  # Renames column head

    def ticket_photo(self, obj):
        return mark_safe(
            '<img src="{}" title="{}" height="300px"/>'.format(
                obj.ticket.image.url, obj.ticket.title
            )
        )

    ticket_photo.admin_order_field = "image"  # Allows column order sorting
    ticket_photo.short_description = "Vignette"  # renames column head

    def has_add_permission(self, request, obj=None):
        return False
