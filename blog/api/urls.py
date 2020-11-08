from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.CreateBlog.as_view()),
    path("create/<int:pk>/", views.EditBlog.as_view()),
    path("list/", views.BlogView.as_view()),
    path("", views.BlogViewList.as_view()),
    path("<int:pk>/get-likers/", views.GetLikersView.as_view()),
    path("like/<int:pk>/", views.BlogLike.as_view()),
    path("favorite/<int:pk>/", views.FavoriteBllog.as_view()),
    path("list/<int:pk>/", views.BlogDetailView.as_view()),
    path("list/<int:pk>/image/", views.BlogImagelView.as_view()),
    path("list/<int:pk>/image/1/", views.BlogImagel1View.as_view()),
    path("image/list/", views.ImageListView.as_view()),
]
