from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views as view


router = DefaultRouter()
router.register('', view.PostViewSet)

app_name = 'post'

urlpatterns = [
    path('feed/',
         view.UserFeedView.as_view(),
         name='feed'),
    path('', include(router.urls)),
    path('comment/<uuid:post_id>/',
         view.AddCommentView.as_view(),
         name='add-comment'),
    path('comment/<int:comment_id>/',
         view.ManageCommentView.as_view(),
         name='manage-comment'),
    path('like/<uuid:post_id>/',
         view.LikeView.as_view(),
         name='like'),
    path('comment/like/<int:comment_id>/',
         view.CommentLikeView.as_view(),
         name='like1'),
    path('<uuid:post_id>/get-likers/',
         view.GetLikersView.as_view(),
         name='get-likers'),
]
