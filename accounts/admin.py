from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email']
    search_fields = ['username', 'email']
    fieldsets = (
        (None, {'fields': ('username', 'password','first_name','last_name')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',"is_company","is_student","groups",'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','is_active', 'is_staff', 'is_superuser',"is_company","is_student"),
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('profile')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if not request.user.is_superuser:
            # Limit fields for non-superusers
            fields = ['username', 'email', 'is_active']
        return fields

# admin.site.register(CustomUser)
admin.site.register(CustomUser,CustomUserAdmin)