__author__ = 'egor'

import api.dbaction.dbconnector as dbconnector
from api.dbaction import users


def follow(email1, email2):
    dbconnector.exist_in_db(table="Users", column="email", value=email1)
    dbconnector.exist_in_db(table="Users", column="email", value=email2)

    if email1 == email2:
        raise Exception("User can't follow himself")

    follows = dbconnector.execute_sql(
        'SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
    )

    if len(follows) == 0:
        dbconnector.execute_update('INSERT INTO Followers (follower, followee) VALUES (%s, %s)',
                                   (email1, email2, ))

    user = users.details(email1)
    return user


def unfollow(email1, email2):
    follows = dbconnector.execute_sql(
        'SELECT id FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
    )

    if len(follows) != 0:
        dbconnector.execute_update(
            'DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, )
        )
    else:
        raise Exception("No such following")

    return users.details(email1)


def list_of_followers(email, type, params):
    dbconnector.exist_in_db(table="Users", column="email", value=email)
    if type == "follower":
        where = "followee"
    if type == "followee":
        where = "follower"

    sql = "SELECT " + type + " FROM Followers JOIN Users ON Users.email = Followers." + type + \
          " WHERE " + where + " = %s "

    if "since_id" in params:
        sql += " AND Users.id >= " + str(params["since_id"])
    if "order" in params:
        sql += " ORDER BY Users.name " + params["order"]
    else:
        sql += " ORDER BY Users.name DESC "
    if "limit" in params:
        sql += " LIMIT " + str(params["limit"])

    followers_ids = dbconnector.execute_sql(sql=sql, params=(email, ))

    followers_list = []
    for id in followers_ids:
        id = id[0]
        followers_list.append(users.details(email=id))

    return followers_list
