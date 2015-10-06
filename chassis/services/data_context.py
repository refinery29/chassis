"""Data Source Context Manager"""
# pylint: disable=too-few-public-methods

from tornado import web


class DataSourceConnectionError(web.HTTPError):
    """Data Source Connection Error"""

    def __init__(self, log_message=None, *args, **kwargs):
        super(DataSourceConnectionError, self).__init__(*args, **kwargs)
        self.status_code = 500
        self.log_message = log_message
        self.args = args
        self.reason = kwargs.get('reason', None)

        if 'headers' in kwargs:
            self.headers = kwargs['headers']


class DatasourceContext(object):
    """Data Source Context Manager"""

    def __init__(self, *args, **kwargs):
        pass

    def _get_connection(self):
        """Override this method to set up the connection."""
        raise NotImplementedError

    def _close_connection(self):
        """Override this method to close the connection."""
        raise NotImplementedError

    def insert(self, query, params):
        """Override this method to close the connection."""
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._close_connection()

    def __enter__(self):
        return self._get_connection()
