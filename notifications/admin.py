from django.contrib import admin

from notifications.models import Notification, Company, Target


# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'hash']
    readonly_fields = ['hash']

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ['company', 'user_id']
    list_filter = ['company']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter = ['is_read', 'target__company']
    list_display = ['target', 'short_message', 'is_read', 'create_at']
    list_editable = ['is_read']

    def short_message(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    short_message.short_description = 'Message'
