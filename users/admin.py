from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'nickname', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'nickname')
    ordering = ('created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname', 'profile_img')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)
