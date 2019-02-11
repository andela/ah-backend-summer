import json

from rest_framework import renderers


class ArticleJSONRenderer(renderers.JSONRenderer):
    """The ArticleJSONRenderer returns a Json object of articles
    """
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        # Method is responsible for displaying articles
        return json.dumps({"articles": data})
