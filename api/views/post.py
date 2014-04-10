__author__ = 'egor'

import json

from api.dbaction import posts
from api.views.service import check_required_params, positive_response, get_optional_params,\
    get_related_params, get_getrequest_params, error_response


def create(request):
    request_data = json.loads(request.body)
    required_data = ["user", "forum", "thread", "message", "date"]
    optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
    optional = get_optional_params(request_data=request_data, possible_values=optional_data)
    try:
        check_required_params(data=request_data, required=required_data)
        post = posts.create(date=request_data["date"], thread=request_data["thread"],
                            message=request_data["message"], user=request_data["user"],
                            forum=request_data["forum"], optional=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(post)


def details(request):
    request_data = get_getrequest_params(request)
    required_data = ["post"]
    related = get_related_params(request_data)
    try:
        check_required_params(data=request_data, required=required_data)
        post = posts.details(request_data["post"], related=related)
    except Exception as e:
        return error_response(e.message)
    return positive_response(post)


def post_list(request):
    request_data = get_getrequest_params(request)
    identifier = None
    try:
        identifier = request_data["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = request_data["thread"]
            entity = "thread"
        except KeyError:
            return error_response("error")

    optional = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since"])
    try:
        p_list = posts.list_of_posts(entity=entity, identifier=identifier, related=[], params=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(p_list)


def remove(request):
    request_data = json.loads(request.body)
    required_data = ["post"]
    try:
        check_required_params(data=request_data, required=required_data)
        post = posts.change_deleted_status(post_id=request_data["post"], status=1)
    except Exception as e:
        return error_response(e.message)
    return positive_response(post)


def restore(request):
    request_data = json.loads(request.body)
    required_data = ["post"]
    try:
        check_required_params(data=request_data, required=required_data)
        post = posts.change_deleted_status(post_id=request_data["post"], status=0)
    except Exception as e:
        return error_response(e.message)
    return positive_response(post)


def update(request):
    request_data = json.loads(request.body)
    required_data = ["post", "message"]
    try:
        check_required_params(data=request_data, required=required_data)
        post = posts.update(id=request_data["post"], message=request_data["message"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(post)


def vote(request):
    request_data = json.loads(request.body)
    required_data = ["post", "vote"]
    try:
        check_required_params(data=request_data, required=required_data)
        post = posts.vote(id=request_data["post"], vote=request_data["vote"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(post)
