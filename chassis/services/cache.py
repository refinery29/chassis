"""Redis Cache."""
# pylint: disable=relative-import, missing-docstring, too-few-public-methods

import redis

from chassis.services import data_context


class CacheConnectionError(data_context.DataSourceConnectionError):
    """Cache Connection Error"""


class Cache(data_context.DatasourceContext):
    """Cache context manager

    Stores configuration properties and opens a new connection when called from
    a handler or service using with.

    """

    def __init__(self, *args, **kwargs):
        self.settings = args[0]
        self._pool = redis.ConnectionPool(**self.settings)
        super(Cache, self).__init__(*args, **kwargs)

    def _get_connection(self):
        return redis.StrictRedis(connection_pool=self._pool)

    def _close_connection(self):
        """Finish up.

        No need to close the connection:
        http://stackoverflow.com/questions/12967107/managing-connection-to-redis-from-python
        """
        pass

    def insert(self, query, params):
        """Nothing to implement"""
        # noop
        return


def retrieve_object(cache, template, indexes):
    """Retrieve an object from Redis using a pipeline.

    Arguments:
        template: a dictionary containg the keys for the object and
            template strings for the corresponding redis keys. The template
            string uses named string interpolation format. Example:

            {
                'username': 'user:$(id)s:username',
                'email': 'user:$(id)s:email',
                'phone': 'user:$(id)s:phone'
            }

        indexes: a dictionary containing the values to use to cosntruct the
            redis keys: Example:

            {
                'id': 342
            }

    Returns: a dictionary with the same keys as template, but containing
        the values retrieved from redis, if all the values are retrieved.
        If any value is missing, returns None. Example:

        {
            'username': 'bob',
            'email': 'bob@example.com',
            'phone': '555-555-5555'
        }

    """
    keys = []
    with cache as redis_connection:
        pipe = redis_connection.pipeline()
        for (result_key, redis_key_template) in template.items():
            keys.append(result_key)
            pipe.get(redis_key_template % indexes)
        results = pipe.execute()
    return None if None in results else dict(zip(keys, results))


def set_object(cache, template, indexes, data):
    """Set an object in Redis using a pipeline.

    Only sets the fields that are present in both the template and the data.

    Arguments:
        template: a dictionary containg the keys for the object and
            template strings for the corresponding redis keys. The template
            string uses named string interpolation format. Example:

            {
                'username': 'user:%(id)s:username',
                'email': 'user:%(id)s:email',
                'phone': 'user:%(id)s:phone'
            }

        indexes: a dictionary containing the values to use to cosntruct the
            redis keys: Example:

            {
                'id': 342
            }

        data: a dictionary returning the data to store. Example:

        {
            'username': 'bob',
            'email': 'bob@example.com',
            'phone': '555-555-5555'
        }

    """
    # TODO(mattmillr): Handle expiration times
    with cache as redis_connection:
        pipe = redis_connection.pipeline()
        for key in set(template.keys()) & set(data.keys()):
            pipe.set(template[key] % indexes, str(data[key]))
        pipe.execute()


def delete_object(cache, template, indexes):
    """Delete an object in Redis using a pipeline.

    Deletes all fields defined by the template.

    Arguments:
        template: a dictionary containg the keys for the object and
            template strings for the corresponding redis keys. The template
            string uses named string interpolation format. Example:

            {
                'username': 'user:%(id)s:username',
                'email': 'user:%(id)s:email',
                'phone': 'user:%(id)s:phone'
            }

        indexes: a dictionary containing the values to use to construct the
            redis keys: Example:

            {
                'id': 342
            }


    """
    with cache as redis_connection:
        pipe = redis_connection.pipeline()
        for key in set(template.keys()):
            pipe.delete(template[key] % indexes)
        pipe.execute()


def multi_get(cache, local_list):
    """Get multiple records by a list of keys.

    Arguments:
        cache:
            instance of Cache

        local_list:
            [
                'user:342:username',
                'user:342:email',
                'user:342:phone'
            ]
    """
    with cache as redis_connection:
        return redis_connection.mget(local_list)


def set_value(cache, key, value):
    """Set a value by key.

    Arguments:
        cache:
            instance of Cache

        key:
            'user:342:username',
    """
    with cache as redis_connection:
        return redis_connection.set(key, value)


def delete_value(cache, *key):
    """Delete a value by key.

    Arguments:
        cache:
            instance of Cache

        key:
            'user:342:username',
    """
    with cache as redis_connection:
        return redis_connection.delete(*key)


def get_value(cache, key):
    """Get a value by key.

    Arguments:
        cache:
            instance of Cache

        key:
            'user:342:username',
    """
    with cache as redis_connection:
        return redis_connection.get(key)
