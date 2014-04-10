__author__ = 'egor'

import api.dbaction.dbconnector as dbconnector
from api.dbaction import users


def forum_desc(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


def forum_save(name, short_name, user):
    dbconnector.exist_in_db(table="Users", column="email", value=user)
    forum = dbconnector.execute_sql(
        'SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        dbconnector.execute_update('INSERT INTO Forums (name, short_name, user) VALUES (%s, %s, %s)',
                                   (name, short_name, user, ))
        forum = dbconnector.execute_sql(
            'SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
        )
    return forum_desc(forum)


def forum_details(short_name, related):
    forum = dbconnector.execute_sql(
        'SELECT id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, )
    )
    if len(forum) == 0:
        raise ("No forum with short_name " + short_name)
    forum = forum_desc(forum)

    if "user" in related:
        forum["user"] = users.details(forum["user"])
    return forum


def list_of_users(short_name, optional):
    dbconnector.exist_in_db(table="Forums", column="short_name", value=short_name)

    sql = "SELECT distinct email FROM Users JOIN Posts ON Posts.user = Users.email " \
          " JOIN Forums on Forums.short_name = Posts.forum WHERE Posts.forum = %s "
    if "since_id" in optional:
        sql += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        sql += " ORDER BY Users.id " + optional["order"]
    if "limit" in optional:
        sql += " LIMIT " + str(optional["limit"])

    users_emails = dbconnector.execute_sql(sql, (short_name, ))
    users_list = []
    for user in users_emails:
        user = user[0]
        users_list.append(users.details(user))
    return users_list
