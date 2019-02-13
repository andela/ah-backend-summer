from django.urls import path

from .views import (
    CommentApiView,
    CommentDetailApiView,
    CommentReplyApiView,
    CommentReplyDetailApiView,
    CommentEditHistoryAPIView,
    CommentReplyEditHistoryAPIView
)


app_name = "comments"

urlpatterns = [
    path('<slug>', CommentApiView.as_view(), name='comments'),
    path('comment-details/<int:pk>',
         CommentDetailApiView.as_view(), name='comment-details'),
    path('comment-reply/<int:comment_pk>',
         CommentReplyApiView.as_view(), name='comment-reply'),
    path(
        'comment-reply-details/<int:pk>',
        CommentReplyDetailApiView.as_view(),
        name='comment-reply-details'
    ),
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
]
