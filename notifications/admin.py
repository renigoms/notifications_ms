from django.contrib import admin

from notifications.models import Notification, Enterprise, Target


# Register your models here.

@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['name', 'hash']
    readonly_fields = ['hash']

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ['enterprise', 'user_id']
    list_filter = ['enterprise']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter = ['is_read', 'target__enterprise']
    list_display = ['target', 'message', 'is_read', 'create_at']
    list_editable = ['is_read']
