"""Utility Encoders for Chassis Applications."""

import json


class ModelJSONEncoder(json.JSONEncoder):
    """Override the default encoder in calls to json.dumps."""

    def default(self, obj):  # pylint: disable=method-hidden
        """Use the default behavior unless the object to be encoded has a
        `strftime` attribute."""

        if hasattr(obj, 'strftime'):
            return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif hasattr(obj, 'get_public_dict'):
            return obj.get_public_dict()
        else:
            return json.JSONEncoder.default(self, obj)
