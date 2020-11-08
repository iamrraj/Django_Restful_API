from django.contrib import admin
from .models import User, UserActivityLogging,ForgottenPasswordToken,UserPasswordHistory


class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ["username", "fullname", "is_staff", "is_active", "email"]
    list_filter = ["is_staff", "is_active"]
    date_hierarchy = "date_joined"
    search_fields = ["username", "fullname"]


admin.site.register(User, UserFeedbackAdmin)


class UserActivityLoggingAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'user', 'event_type', 'endpoint',
                    'response_status', 'is_response_ok', 'request_method']
    list_filter = ['created_at', 'request_method', 'response_status']
    date_hierarchy = 'created_at'
    search_fields = ['created_at', 'event_type',
                     'request_method', 'response_status']

    def user(self, obj):
        return obj.user if obj.user else 'Unauthenticated user'

    def is_response_ok(self, obj):
        return '200' in obj.response_status in obj.response_status
    is_response_ok.boolean = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(UserActivityLogging, UserActivityLoggingAdmin)


class PasswordLoggingAdmin(admin.ModelAdmin):
    list_display = ['user' ,'series','success', 'ip_address', 'token_end_date', 'token_value',
                    'ts']
    list_filter = ['ts', 'user']
    date_hierarchy = 'ts'
    search_fields = ['user']


admin.site.register(ForgottenPasswordToken, PasswordLoggingAdmin)


class UserPasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ['user' ,'password','created_at']
    list_filter = [ 'user']
    date_hierarchy = 'created_at'
    search_fields = ['user']


admin.site.register(UserPasswordHistory, UserPasswordHistoryAdmin)
