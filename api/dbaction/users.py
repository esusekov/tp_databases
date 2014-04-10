__author__ = 'egor'

from api.dbaction import dbconnector
from api.dbaction.service import column_to_list as ctl


def user_desc(user):
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response


def select_user(sql, params):
    return dbconnector.execute_sql(sql, params)


def user_save(email, username, about, name, optional):
    isAnonymous = 0
    if "isAnonymous" in optional:
        isAnonymous = optional["isAnonymous"]
    try:
        user = select_user('SELECT email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
        if len(user) == 0:
            dbconnector.execute_update(
                'INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, ))
        user = select_user('SELECT email, about, isAnonymous, id, name, username FROM Users WHERE email = %s',
                           (email, ))
    except Exception as e:
        raise Exception(e.message)

    return user_desc(user)


def user_update(email, about, name):
    dbconnector.exist_in_db(table="Users", column="email", value=email)
    dbconnector.execute_update('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s',
                          (email, about, name, email, ))
    return details(email)


def followers(email, type):
    where = "followee"
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"
    f_list = dbconnector.execute_sql(
        "SELECT " + type + " FROM Followers JOIN Users ON Users.email = Followers." + type +
        " WHERE " + where + " = %s ", (email, )
    )
    return ctl(f_list)


def details(email):
    user = user_query(email)
    if user is None:
        raise Exception("No such user")
    user["followers"] = followers(email, "follower")
    user["following"] = followers(email, "followee")
    user["subscriptions"] = user_subscriptions(email)
    return user


def user_subscriptions(email):
    subscriptions = dbconnector.execute_sql('SELECT thread FROM Subscriptions WHERE user = %s', (email, ))
    return ctl(subscriptions)


def user_query(email):
    user = select_user('SELECT email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, ))
    if len(user) == 0:
        return None
    return user_desc(user)

