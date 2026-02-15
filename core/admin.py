from django.contrib import admin
from .models import FBGroup

@admin.register(FBGroup)
class FBGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_set', 'group_url')
    list_filter = ('group_set',)
    search_fields = ('name',)
    fieldsets = (
        ('Group Information', {
            'fields': ('name', 'group_set')
        }),
        ('Links', {
            'fields': ('group_url',)
        }),
    )
