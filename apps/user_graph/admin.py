from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserFollows
from apps.user.models import User

# admin.site.register(UserFollows)


class UserFollowingInline(admin.TabularInline):
    model = UserFollows
    fk_name = "user"

    extra = 0

    verbose_name = "Abonnement"
    verbose_name_plural = "Abonnements"


class UserFollowedInline(admin.TabularInline):
    model = UserFollows
    fk_name = "followed_user"

    extra = 0

    verbose_name = "Abonné"
    verbose_name_plural = "Abonnés"


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [UserFollowingInline, UserFollowedInline]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                ]
            },
        ),
        (
            "Contrôle des accès",
            {
                "classes": [
                    "collapse",
                ],
                "fields": ["is_active", "is_staff", "is_superuser"],
            },
        ),
        (
            "Dates",
            {
                "fields": ["date_joined", "last_login"],
            },
        ),
    ]
    readonly_fields = ["date_joined", "last_login"]

    list_display = (
        "username",
        "email",
    )
    list_filter = ("is_active",)
