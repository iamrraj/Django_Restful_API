from django.urls import path, include
from . import views


urlpatterns = [
    path('resume/', views.ResumeView.as_view()),
    path('resume/<int:pk>/', views.ResumeViewDetail.as_view()),
    path('resume/user/', views.ResumeViewUser.as_view()),
]
