from rest_framework.pagination import LimitOffsetPagination


class ArticleLimitOffsetPagination(LimitOffsetPagination):
    """ Class that will set article endpoint to only
    only 10 articles per page
    """

    default_limit = 10
    offset_query_param = "offset"
