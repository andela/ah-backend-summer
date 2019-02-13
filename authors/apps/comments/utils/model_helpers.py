import timeago
from django.utils import timezone


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
