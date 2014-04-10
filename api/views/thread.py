__author__ = 'egor'

import json

from api.dbaction import threads, posts, subscriptions
from api.views.service import positive_response, get_related_params, check_required_params,\
    get_optional_params, get_getrequest_params, error_response


def create(request):
    request_data = json.loads(request.body)
    required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
    optional = get_optional_params(request_data=request_data, possible_values=["isDeleted"])
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.save_thread(forum=request_data["forum"], title=request_data["title"], isClosed=request_data["isClosed"],
                                 user=request_data["user"], date=request_data["date"], message=request_data["message"],
                                 slug=request_data["slug"], optional=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def details(request):
    request_data = get_getrequest_params(request)
    required_data = ["thread"]
    related = get_related_params(request_data)
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.details(id=request_data["thread"], related=related)
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def vote(request):
    request_data = json.loads(request.body)
    required_data = ["thread", "vote"]
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.vote(id=request_data["thread"], vote=request_data["vote"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def subscribe(request):
    request_data = json.loads(request.body)
    required_data = ["thread", "user"]
    try:
        check_required_params(data=request_data, required=required_data)
        subscription = subscriptions.add_subscription(email=request_data["user"], thread_id=request_data["thread"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(subscription)


def unsubscribe(request):
    request_data = json.loads(request.body)
    required_data = ["thread", "user"]
    try:
        check_required_params(data=request_data, required=required_data)
        subscription = subscriptions.delete_subscription(email=request_data["user"], thread_id=request_data["thread"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(subscription)


def open(request):
    request_data = json.loads(request.body)
    required_data = ["thread"]
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.change_closed_status(id=request_data["thread"], isClosed=0)
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def close(request):
    request_data = json.loads(request.body)
    required_data = ["thread"]
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.change_closed_status(id=request_data["thread"], isClosed=1)
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def update(request):
    request_data = json.loads(request.body)
    required_data = ["thread", "slug", "message"]
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.update_thread(id=request_data["thread"], slug=request_data["slug"], message=request_data["message"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def remove(request):
    request_data = json.loads(request.body)
    required_data = ["thread"]
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.change_deleted_status(thread_id=request_data["thread"], status=1)
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def restore(request):
    request_data = json.loads(request.body)
    required_data = ["thread"]
    try:
        check_required_params(data=request_data, required=required_data)
        thread = threads.change_deleted_status(thread_id=request_data["thread"], status=0)
    except Exception as e:
        return error_response(e.message)
    return positive_response(thread)


def thread_list(request):
    request_data = get_getrequest_params(request)
    identifier = None
    try:
        identifier = request_data["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = request_data["user"]
            entity = "user"
        except KeyError:
            return error_response("No params setted")
    optional = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since"])
    try:
        t_list = threads.list_of_threads(entity=entity, identificator=identifier, related=[], params=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(t_list)


def list_posts(request):
    request_data = get_getrequest_params(request)
    required_data = ["thread"]
    entity = "thread"
    optional = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since"])
    try:
        check_required_params(data=request_data, required=required_data)
        p_list = posts.list_of_posts(entity=entity, identifier=request_data["thread"], related=[], params=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(p_list)
