
from django.urls import path, re_path as url
from . import views


urlpatterns = [
    path(r'subscribe/confirm/', views.subscription_confirmation, name='subscription_confirmation'),
    path(r'unsubscribe/', views.unsubscribe, name='unsubscribe'),   
]





