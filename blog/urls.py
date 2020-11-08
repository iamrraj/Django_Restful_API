from django.urls import path, re_path as url
from . import views


urlpatterns = [
    url(r"^email/tr-(?P<key>.*)\.png$", views.email_seen, name="driver_email_seen"),
    path("email/preview/<int:pk>/", views.preview_email, name="driveremail_preview"),
    path("email/test/<int:pk>/", views.test_email, name="driveremail_test"),
]

