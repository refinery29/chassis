"""Test Utility Encoders."""
# pylint: disable=missing-docstring

import datetime
import mock
import unittest

from chassis.util import encoders


class TestModelJSONEncoder(unittest.TestCase):

    @mock.patch('json.JSONEncoder')
    def test_obj_with_strftime(self, unused_mock):

        obj = datetime.datetime(2015, 8, 29, 17, 30)
        expected = "2015-08-29T17:30:00Z"

        encoder = encoders.ModelJSONEncoder()
        result = encoder.default(obj)

        self.assertEquals(result, expected)

    @mock.patch('json.JSONEncoder')
    def test_obj_with_get_public_dict(self, unused_mock):

        obj = mock.Mock()
        del obj.strftime
        obj.get_public_dict = mock.Mock()
        obj.get_public_dict.return_value = 'foo'

        encoder = encoders.ModelJSONEncoder()
        result = encoder.default(obj)

        self.assertEquals(result, 'foo')
        obj.get_public_dict.assert_called_with()

    @mock.patch('json.JSONEncoder')
    def test_obj_default(self, mock_json_encoder):

        obj = object()

        mock_json_encoder.default = mock.Mock()
        mock_json_encoder.default.return_value = 'foo'

        encoder = encoders.ModelJSONEncoder()
        result = encoder.default(obj)

        self.assertEquals(result, 'foo')
        mock_json_encoder.default.assert_called_with(encoder, obj)
