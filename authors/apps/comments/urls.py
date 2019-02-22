from django.urls import path

from .views import (
    CommentApiView,
    CommentDetailApiView,
    CommentReplyApiView,
    CommentReplyDetailApiView,
    CommentEditHistoryAPIView,
    CommentReplyEditHistoryAPIView,
    LikeCommentApiView,
    DislikeCommentApiView
)

app_name = "comments"

urlpatterns = [
    path('comments/<int:comment_pk>/replies',
         CommentReplyApiView.as_view(), name='comment-reply'),
    path(
        '<str:slug>/comment/<int:pk>/history',
        CommentEditHistoryAPIView.as_view(),
        name='comment-edit-history'
    ),
    path(
        '<int:comment_pk>/comment-reply/<int:pk>/history',
        CommentReplyEditHistoryAPIView.as_view(),
        name='comment-reply-edit-history'
    ),
    path('comments/replies/<int:pk>',
         CommentReplyDetailApiView.as_view(),
         name='comment-reply-details'
         ),
    path('comments/<int:pk>',
         CommentDetailApiView.as_view(), name='comment-details'),
    path('<str:slug>/comments', CommentApiView.as_view(), name='comments'),
    path('comments/<int:pk>/like', LikeCommentApiView.as_view(),
         name='comment-likes'),
    path('comments/<int:pk>/dislike', DislikeCommentApiView.as_view(),
         name='comment-dislikes')
]
