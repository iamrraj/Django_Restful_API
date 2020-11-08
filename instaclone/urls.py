"""instagram1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path as url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
import user.views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import (
    FCMDeviceAuthorizedViewSet,
)  # this package for push notifications and messages


router = DefaultRouter()
router.register(r"devices", FCMDeviceAuthorizedViewSet)


admin.site.site_title = "Rahul API"
admin.site.index_title = "Admin"
admin.site.site_header = "Rahul API Administration"


schema_view = get_schema_view(
    openapi.Info(
        title="Instagram Clone API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r"^jet/", include("jet.urls", "jet")),  # Django JET URLS
    url(
        r"^jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
    ),  # Django JET dashboard URLS
    path("admin/", admin.site.urls),
    path("id/", include(router.urls)),
    path("tinymce/", include("tinymce.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/confirm/<key>/", user.views.confirm, name="users_confirm"),
    path("users/password-reset/", csrf_exempt(user.views.PasswordReset.as_view())),
    path(
        "api/1/oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")
    ),  # Login Endpoin
    url(
        r"^api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("api/1/user/", include("user.api.urls")),
    path("api/1/post/", include("Post.api.urls")),
    path("api/1/blog/", include("blog.api.urls")),
    path("api/1/data/", include("data1.api.urls")),
    path("", include("blog.urls")),
    # Swagger Api endpoint
    url(r"^face_detection/detect/$", "face.views.detect"),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
