from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    ordering = ('-data_joined',)
    search_fields = ['email', 'user_name', 'first_name', 'last_name']
    list_display = ['email', 'user_name', 'first_name', 'last_name', 'is_staff', 'is_superuser']
    list_filter = ['data_joined', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'user_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'phone_number', 'confirm')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'password1', 'password2', 'is_staff')}
         ),
    )


admin.site.register(Profile, UserAdminConfig)
