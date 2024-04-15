from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phoneNumber', 'isActive']
    list_filter = ['isActive']
    search_fields = ['name', 'phoneNumber']
    search_help_text = "Search By 'Name' and 'Phone number' field"

# admin.site.register(User, UserAdmin)
