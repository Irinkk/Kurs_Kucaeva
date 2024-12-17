from django.contrib import admin
from .models import CustomUser,Category,Ad

admin.site.register(Category)
admin.site.register(Ad)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_client', 'is_moderator', 'is_staff')
    list_filter = ('is_client', 'is_moderator', 'is_staff')
    search_fields = ('email',)