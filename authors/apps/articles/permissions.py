from rest_framework import permissions


class IsAuthorOfTheArticle(permissions.BasePermission):
    """IsAuthorOfArticle is a custom class that checks to
    see if the user trying to update or delete an article
    is the aurtor of the article
    """
    message = "This article does not belong to you. Access denied"

    def has_object_permission(self, request, view, obj):
        # Grants users permissions for read-only requests
        if request.method is "GET":
            return True
        # Grants user permission to edit or delete object if they're the
        # authors of the article.
        return obj.author.user == request.user
