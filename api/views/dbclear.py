__author__ = 'egor'

from api.dbaction import dbclear

from api.views.service import positive_response, error_response


def clear(request):
    try:
        response = dbclear.clear()
    except Exception as e:
        return error_response(e.message)
    return positive_response(response)