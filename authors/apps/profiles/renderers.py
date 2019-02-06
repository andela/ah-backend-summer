import json
from rest_framework import renderers


class ProfileRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        # Method is responsible for displaying user profile
        # and errors if they exist
        errors = data.get("errors")

        if errors:
            return super().render(data)
        return json.dumps({"profile": data})
