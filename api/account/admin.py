from django.contrib import admin

from account import models


@admin.register(models.Email)
class EmailAdmin(admin.ModelAdmin):
    """
    Admin for the Email model.
    """
    fields = (
        'address',
        'user',
        'is_verified',
        'time_created',
        'time_updated',
    )
    list_display = ('address', 'user', 'is_verified')
    search_fields = ('address', 'user__name')
