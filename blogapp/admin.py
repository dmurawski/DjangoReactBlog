from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Blog, CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name")


admin.site.register(CustomUser, CustomUserAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "is_draft", "created_at", "category")


admin.site.register(Blog, BlogAdmin)
