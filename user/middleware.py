from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.admin.models import LogEntry

event_type = ''


def get_event_type(request, response):
    if 'admin/logout' in request.path:
        return 'USER_LOGGING_OUT'
    if 'admin/login' in request.path and request.method == 'POST':
        return 'USER_LOGGING_IN_ATTEMPT'
    if 'admin/password_change' in request.path and request.method == 'POST':
        return 'USER_RESET_PASSWORD_ATTEMPT'
    if 'registration' in request.path and request.method == 'POST':
        if response.status_code == 200:
            return 'USER_REGISTRATION_SUCCESSFUL'
        return 'USER_REGISTRATION_FAILED'
    if 'auth/user/add/' in request.path and request.method == 'POST':
        return 'CREATED_USER_ACCOUNT_ATTEMPT'
    if 'admin/' in request.path and 'auth/' in request.path and '/change/' in request.path:
        if request.method == 'POST':
            return 'MODIFIED_USER_ACCOUNT_ATTEMPT'
    if 'admin/auth/user/' in request.path and request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'delete_selected':
            return 'DELETED_USER_ACCOUNT_ATTEMPT'
    if 'update-password' in request.path and request.method == 'PUT':
        if response.status_code == 200:
            return 'USER_RESET_PASSWORD_SUCCESSFUL'
        return 'USER_RESET_PASSWORD_FAILED'
    if 'oauth/token/dashboard' in request.path and request.method == 'POST':
        if response.status_code == 200:
            return 'USER_LOGGING_IN_SUCCESSFUL'
        if response.status_code == 403:
            return 'USER_LOGGING_IN_BLOCKED'
        if response.status_code == 401:
            return 'USER_LOGGING_IN_FAILED_UNAUTHORIZED'
        return 'USER_LOGGING_IN_FAILED'
    if 'export' in request.path or 'report' in request.path:
        return 'DATA_EXPORT'
    return 'BROWSING_READ_DATA'


def get_user_ipv4(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(post_save)
def receiver_on_object_post_save(sender, instance, created, **kwargs):
    if sender.__name__ == LogEntry.__name__ or sender.__name__ == UserActivityLogging.__name__:
        return
    global event_type
    if created:
        event_type = 'CREATED_OBJECT %s(%s)' % (sender.__name__, instance.pk)
    else:
        event_type = 'MODIFIED_OBJECT %s(%s)' % (sender.__name__, instance.pk)


@receiver(post_delete)
def receiver_on_object_post_delete(sender, instance, **kwargs):
    if sender.__name__ == LogEntry.__name__ or sender.__name__ == UserActivityLogging.__name__:
        return
    global event_type
    event_type = 'DELETED_OBJECT %s(%s)' % (sender.__name__, instance.pk)


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        """
        print('user = %s' % request.user)
        print('event type = %s' % get_event_type(request, response))
        print('url = %s' % request.get_full_path())
        print('request content_type = %s' % request.content_type)
        print('response content_type = %s' % response['Content-Type'])
        """

        user = None
        if hasattr(request, 'user'):
            user = request.user
        # if user:
        #     if user.username == 'rahul@vivadrive.io':
        #         return response
        response_content_type = response['Content-Type']
        if 'text/html' in response_content_type or 'text/plain' in response_content_type or 'application/json' in response_content_type:
            try:
                global event_type
                ua = UserActivityLogging.objects.create(
                    user=user, endpoint=request.path)
                ua.event_type = event_type if (
                    event_type and request.method != 'GET') else get_event_type(request, response)
                ua.request_method = request.method
                ua.response_status = "%d, %s" % (
                    response.status_code, response.reason_phrase)
                ua.response_content_type = response_content_type
                ua.user_ipv4 = get_user_ipv4(request)
                ua.save()
            except Exception as e:
                print(str(e))

        return response
