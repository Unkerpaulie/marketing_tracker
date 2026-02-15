from django.contrib import admin
from .models import Post, Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'post_count')
    list_filter = ('created_at',)
    search_fields = ('name', 'text')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Ad Information', {
            'fields': ('name', 'text')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('ad', 'fb_group', 'posted_at', 'last_updated', 'engagement_count')
    list_filter = ('posted_at', 'fb_group', 'ad')
    search_fields = ('ad__name', 'fb_group__name')
    readonly_fields = ('last_updated', 'engagement_count')
    fieldsets = (
        ('Post Information', {
            'fields': ('ad', 'fb_group', 'post_url')
        }),
        ('Timestamps', {
            'fields': ('posted_at', 'last_updated'),
            'classes': ('collapse',)
        }),
        ('Engagement', {
            'fields': ('engagement_count',),
            'classes': ('collapse',)
        }),
    )

    def engagement_count(self, obj):
        return obj.engagements.count()
    engagement_count.short_description = 'Total Engagements'
