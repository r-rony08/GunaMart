from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "role",
        "is_active",
        "is_staff",
    )

    list_filter = ("role", "is_active", "is_staff",)

    search_fields = ("email", "username", "first_name", "last_name", "phone_number")

    ordering = ("-date_joined",)

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Personal Information", {
            "fields": (
                "username",
                "first_name",
                "last_name",
                "phone_number",
            )
        }),
        ("Role & Status", {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),
        ("Permissions", {
            "fields": (
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "first_name",
                "last_name",
                "phone_number",
                "role",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )

