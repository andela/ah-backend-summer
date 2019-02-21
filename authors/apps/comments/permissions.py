from rest_framework import permissions


class IsOwnerOfCommentOrReply(permissions.BasePermission):
    """IsAuthorOfArticle is a custom class that checks to
    see if the user trying to get edit history of a comment or
    reply is the actual owner
    """
    message = "Access denied, you cant view edit history for a\
comment or reply you didnt create"

    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user
