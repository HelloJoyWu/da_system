import logging
from functools import wraps

from django.db import connections

logger = logging.getLogger(__name__)


def maria_read_trigger_setter(
        default_result=None,
        error_display_args: bool = True
):
    """
    # TODO: Not using; let django to catch the error directly
    Passing parameters to the decorator when calling query function which need maria connection.
    The decorator is applied to catch the exception and giving connection object to the function.
    :param default_result: the result when exception is raised
    :param error_display_args: to display the args and kwargs of query function ot not
    :return: decorator with setted parameters
    """

    def maria_read_trigger(query_fn) -> default_result:

        @wraps(maria_read_trigger)
        def wrap(*args, **kwargs):

            result = default_result
            try:

                with connections['maria_read'].cursor() as cursor:
                    kwargs['cursor'] = cursor
                    return query_fn(*args, **kwargs)

            except Exception as e:

                err_msg = f'{query_fn.__module__}.{query_fn.__name__} failed '
                if error_display_args:
                    err_msg += f'with args: {args}, and kwargs: {kwargs}: '
                # logger.error(get_err_txt(e))
                logger.debug(f'origin error: \n{e}')
                return result

        return wrap
    return maria_read_trigger