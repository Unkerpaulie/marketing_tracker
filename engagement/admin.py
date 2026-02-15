from django.contrib import admin
from .models import Contact, Engagement

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'engagement_count', 'fb_url')
    search_fields = ('name',)
    readonly_fields = ('engagement_count',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'fb_url')
        }),
        ('Engagement Stats', {
            'fields': ('engagement_count',),
            'classes': ('collapse',)
        }),
    )

    def engagement_count(self, obj):
        return obj.engagements.count()
    engagement_count.short_description = 'Total Engagements'

@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ('contact', 'post', 'created_at', 'content_preview')
    list_filter = ('created_at', 'contact', 'post__ad')
    search_fields = ('contact__name', 'content', 'post__ad__name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Engagement Information', {
            'fields': ('contact', 'post')
        }),
        ('Content', {
            'fields': ('content', 'notes')
        }),
        ('Links', {
            'fields': ('message_url',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
