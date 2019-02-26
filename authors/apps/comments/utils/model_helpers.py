import timeago
from django.utils import timezone
from rest_framework import status


def get_single_comment_using_id(obj, id):
    """
    Method is a helper that retrieves an object or model
    record basing on the model passed and the id provided
    """
    try:
        comment = obj.objects.get(pk=id)
        return comment
    except obj.DoesNotExist:
        return None


def get_comment_edit_history(obj, id):
    """
    This method gets edit history for a comment or comment
    reply
    """
    comment = get_single_comment_using_id(obj, id)
    if comment:
        comment_history = comment.edit_history.all()
        return get_comment_history(comment)


def get_comment_history(comment):
    """
    This method creates a dictionary of an edit history for
    a comment or comment reply
    """
    edit_history_list = []
    history = comment.edit_history.all()
    now = timezone.now()
    current_time = now.strftime("%d-%m-%y %H:%M:%S")
    for edit in list(history):
        edit_history_type = "original comment"
        if edit.history_type == "~":
            edit_history_type = "modified"
        history_time = edit.updated_at.strftime(
            "%d-%m-%y %H:%M:%S")
        edit_history_info = {
            "date": timezone.localtime(
                edit.updated_at).strftime(
                    "%d-%m-%y %H:%M"),
            "history_date": timeago.format(
                history_time, current_time
            ),
            "history_change_type": edit_history_type,
            "comment_body": str(edit.body)
        }
        edit_history_list.append(edit_history_info)
    return edit_history_list


def check_if_user_is_object_author(obj, user):
    return obj.author.user == user


class LikeDislikeObject():
    """
    This class has methods that handle liking, disliking,
    un-liking, un-disliking of a comment
    """

    def __init__(self, request, model,
                 pk, object_type, action):
        self.request = request
        self.model = model
        self.pk = pk
        self.object_type = object_type
        self.action = action
        self.obj = get_single_comment_using_id(
            self.model, self.pk
        )
        if self.obj:
            self.is_author = check_if_user_is_object_author(
                self.obj, request.user
            )

    def action_is_active(self):
        if self.action == "like" and (
                self.request.user in self.obj.liked_by.all()):
            status = True
        elif self.action == "dislike" and (
                self.request.user in self.obj.disliked_by.all()):
            status = True
        else:
            status = False
        return status

    def opposite_is_active(self):
        if self.action == "like" and (
                self.request.user in self.obj.disliked_by.all()):
            opposite_status = True
        elif self.action == "dislike" and (
                self.request.user in self.obj.liked_by.all()):
            opposite_status = True
        else:
            opposite_status = False
        return opposite_status

    def add_action(self):
        if self.action == "like":
            self.obj.liked_by.add(self.request.user)
        elif self.action == "dislike":
            self.obj.disliked_by.add(self.request.user)

    def remove_action(self):
        if self.action == "like":
            self.obj.liked_by.remove(self.request.user)
        elif self.action == "dislike":
            self.obj.disliked_by.remove(self.request.user)

    def remove_opposite_action(self):
        if self.action == "like":
            self.obj.disliked_by.remove(self.request.user)
        elif self.action == "dislike":
            self.obj.liked_by.remove(self.request.user)

    def get_status_of_action_for_obj(self):
        if self.obj:
            action_status = self.action_is_active()
            data = {
                f'{self.action} status:': action_status,
                "message": f"Success! {self.object_type} pk': {self.pk}",
                "status": 200
            }
            status_code = status.HTTP_200_OK
        else:
            data = {
                "message": f"Failed! Error: {self.object_type} \
with pk: {self.pk} does not exist!",
                "status": 404
            }
            status_code = status.HTTP_404_NOT_FOUND
        return data, status_code

    def perform_action_on_object(self):
        if not self.obj:
            data = {
                "message": f"Failed! Error: {self.object_type} \
with pk: {self.pk} does not exist!",
                "status": 404
            }
            status_code = status.HTTP_404_NOT_FOUND

        elif self.action_is_active() is True:
            data = {
                "message": f"Failed! You already {self.action} \
{self.object_type} with pk {self.pk}",
                "status": 400
            }
            status_code = status.HTTP_400_BAD_REQUEST

        elif self.is_author is True:
            data = {
                "message": f"Failed! You cannot {self.action} a \
{self.object_type} you authored",
                "status": 400
            }
            status_code = status.HTTP_400_BAD_REQUEST

        elif self.opposite_is_active() is True:
            self.remove_opposite_action()
            self.add_action()
            data = {
                "message": f"Success! You have changed your action \
to {self.action} {self.object_type} with pk {self.pk}",
                "status": 201
            }
            status_code = status.HTTP_201_CREATED

        elif self.action_is_active() is False and self.is_author is False:
            self.add_action()
            data = {
                "message": f"Success! You have a added a \
{self.action} to {self.object_type} with pk {self.pk}",
                "status": 201
            }
            status_code = status.HTTP_201_CREATED
        return data, status_code

    def undo_action_on_object(self):
        if not self.obj:
            data = {
                "message": f"Failed! Error: {self.object_type} \
with pk: {self.pk} does not exist!",
                "status": 404
            }
            status_code = status.HTTP_404_NOT_FOUND

        elif self.action_is_active() is False:
            data = {
                "message": f" Failed! You do not {self.action} \
{self.object_type} with pk {self.pk}",
                "status": 400
            }
            status_code = status.HTTP_400_BAD_REQUEST

        elif self.is_author is True:
            data = {
                "message": f"Failed! You cannot reverse \
{self.action} on {self.object_type} you didn't author",
                "status": 400
            }
            status_code = status.HTTP_400_BAD_REQUEST

        elif self.action_is_active() is True:
            self.remove_action()
            data = {
                "message": f"Success! You have reversed \
{self.action} action on {self.object_type} with pk {self.pk}",
                "status": 200
            }
            status_code = status.HTTP_200_OK
        return data, status_code
