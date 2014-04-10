__author__ = 'egor'

import json

from api.dbaction import users, posts, followers
from api.views.service import positive_response, check_required_params, get_optional_params, \
    get_getrequest_params, error_response


def create(request):
    request_data = json.loads(request.body)
    required_data = ["email", "username", "name", "about"]
    optional = get_optional_params(request_data=request_data, possible_values=["isAnonymous"])
    try:
        check_required_params(data=request_data, required=required_data)
        user = users.user_save(email=request_data["email"], username=request_data["username"],
                               about=request_data["about"], name=request_data["name"], optional=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(user)


def details(request):
    request_data = get_getrequest_params(request)
    required_data = ["user"]
    try:
        check_required_params(data=request_data, required=required_data)
        user_details = users.details(email=request_data["user"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(user_details)


def follow(request):
    request_data = json.loads(request.body)
    required_data = ["follower", "followee"]
    try:
        check_required_params(data=request_data, required=required_data)
        following = followers.follow(email1=request_data["follower"], email2=request_data["followee"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(following)


def unfollow(request):
    request_data = json.loads(request.body)
    required_data = ["follower", "followee"]
    try:
        check_required_params(data=request_data, required=required_data)
        following = followers.unfollow(email1=request_data["follower"], email2=request_data["followee"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(following)


def list_followers(request):
    request_data = get_getrequest_params(request)
    required_data = ["user"]
    followers_param = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since_id"])
    try:
        check_required_params(data=request_data, required=required_data)
        follower_l = followers.list_of_followers(email=request_data["user"], type="follower", params=followers_param)
    except Exception as e:
        return error_response(e.message)
    return positive_response(follower_l)


def list_following(request):
    request_data = get_getrequest_params(request)
    required_data = ["user"]
    followers_param = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since_id"])
    try:
        check_required_params(data=request_data, required=required_data)
        followings = followers.list_of_followers(email=request_data["user"], type="followee", params=followers_param)
    except Exception as e:
        return error_response(e.message)
    return positive_response(followings)


def list_posts(request):
    request_data = get_getrequest_params(request)
    required_data = ["user"]
    optional = get_optional_params(request_data=request_data, possible_values=["limit", "order", "since"])
    try:
        check_required_params(data=request_data, required=required_data)
        posts_l = posts.list_of_posts(entity="user", identifier=request_data["user"], related=[], params=optional)
    except Exception as e:
        return error_response(e.message)
    return positive_response(posts_l)


def update(request):
    request_data = json.loads(request.body)
    required_data = ["user", "name", "about"]
    try:
        check_required_params(data=request_data, required=required_data)
        user = users.user_update(email=request_data["user"], name=request_data["name"], about=request_data["about"])
    except Exception as e:
        return error_response(e.message)
    return positive_response(user)
