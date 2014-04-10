__author__ = 'egor'

import json

from api.dbaction import forums, threads, posts

from api.views.service import get_related_params, positive_response, check_required_params, \
    get_optional_params, get_getrequest_params, error_response


def create(request):
    request_data = json.loads(request.body)
    required_data = ["name", "short_name", "user"]
    try:
        check_required_params(data=request_data, required=required_data)
        forum = forums.forum_save(name=request_data["name"], short_name=request_data["short_name"],
                                  user=request_data["user"])
    except Exception as e:
        print("name = " + request_data["name"])
        print("short_name = " + request_data["short_name"])
        print("user = " + request_data["user"])
        print(e.message)
        return error_response(e.message)
    return positive_response(forum)


def details(request):
    request_data = get_getrequest_params(request)
    required_data = ["forum"]
    related = get_related_params(request_data)
    try:
        check_required_params(data=request_data, required=required_data)
        forum = forums.forum_details(short_name=request_data["forum"], related=related)
    except Exception as e:
        return error_response(e.message)
    return positive_response(forum)


def list_threads(request):
    request_data = get_getrequest_params(request)
    required_data = ["forum"]
    related = get_related_params(request_data)
    optional = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since"])
    try:
        check_required_params(data=request_data, required=required_data)
        threads_l = threads.list_of_threads(entity="forum", identificator=request_data["forum"],
                                         related=related, params=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(threads_l)


def list_posts(request):
    request_data = get_getrequest_params(request)
    required_data = ["forum"]
    related = get_related_params(request_data)

    optional = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since"])
    try:
        check_required_params(data=request_data, required=required_data)
        posts_l = posts.list_of_posts(entity="forum", identifier=request_data["forum"],
                                   related=related, params=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(posts_l)


def list_users(request):
    request_data = get_getrequest_params(request)
    required_data = ["forum"]
    optional = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since_id"])
    try:
        check_required_params(data=request_data, required=required_data)
        users_l = forums.list_of_users(request_data["forum"], optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(users_l)
