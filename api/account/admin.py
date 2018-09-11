from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from account import models


@admin.register(models.Email)
class EmailAdmin(admin.ModelAdmin):
    """
    Admin for the Email model.
    """
    autocomplete_fields = ('user',)
    fields = (
        'address',
        'user',
        'is_verified',
        'time_created',
        'time_updated',
    )
    list_display = ('address', 'user', 'is_verified')
    list_filter = ('is_verified',)
    readonly_fields = ('time_created', 'time_updated')
    search_fields = ('address', 'user__name')


class UserAddForm(UserCreationForm):
    class Meta:
        fields = ('name',)
        model = models.User


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('name', 'password1', 'password2'),
        }),
    )
    add_form = UserAddForm
    autocomplete_fields = ('primary_email',)
    date_hierarchy = 'time_created'
    fieldsets = (
        (None, {
            'fields': ('name', 'password'),
        }),
        (_('Personal Information'), {
            'fields': ('primary_email',),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
    )
    list_display = (
        'name',
        'primary_email',
        'is_active',
        'is_staff',
        'is_superuser',
        'time_created',
    )
    ordering = None
    search_fields = ('name',)
