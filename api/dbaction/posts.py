__author__ = 'egor'

from api.dbaction import dbconnector
from api.dbaction.dbconnector import DBConnection
from api.dbaction import users, forums, threads


def post_desc(post):
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],

    }
    return post_response


def details(id, related):
    post = post_query(id)
    if post is None:
        raise Exception("no post with id = " + id)

    if "user" in related:
        post["user"] = users.details(post["user"])
    if "forum" in related:
        post["forum"] = forums.forum_details(short_name=post["forum"], related=[])
    if "thread" in related:
        post["thread"] = threads.details(id=post["thread"], related=[])

    return post

def create(date, thread, message, user, forum, optional):
    dbconnector.exist_in_db(table="Threads", column="id", value=thread)
    dbconnector.exist_in_db(table="Forums", column="short_name", value=forum)
    dbconnector.exist_in_db(table="Users", column="email", value=user)
    if len(dbconnector.execute_sql("SELECT Threads.id FROM Threads JOIN Forums ON Threads.forum = Forums.short_name "
                                   "WHERE Threads.forum = %s AND Threads.id = %s", (forum, thread, ))) == 0:
        raise Exception("No such thread")
    if "parent" in optional:
        if len(dbconnector.execute_sql("SELECT Posts.id FROM Posts JOIN Threads ON Threads.id = Posts.thread "
                                       "WHERE Posts.id = %s AND Threads.id = %s", (optional["parent"], thread, ))) == 0:
            raise Exception("No post with id = " + optional["parent"])
    query = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    parameters = [message, user, forum, thread, date]

    for param in optional:
        query += ", " + param
        values += ", %s"
        parameters.append(optional[param])

    query += ") VALUES " + values + ")"

    update_thread_posts = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"

    connection = DBConnection()
    connection = connection.connect()
    connection.autocommit(False)
    with connection:
        cursor = connection.cursor()
        try:
            connection.begin()
            cursor.execute(update_thread_posts, (thread, ))
            cursor.execute(query, parameters)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception("Database error: " + e.message)
        post_id = cursor.lastrowid
        cursor.close()

    connection.close()
    post = post_query(post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post



def list_of_posts(entity, identifier, related, params):
    if entity == "forum":
        dbconnector.exist_in_db(table="Forums", column="short_name", value=identifier)

    if entity == "thread":
        dbconnector.exist_in_db(table="Threads", column="id", value=identifier)

    if entity == "user":
        dbconnector.exist_in_db(table="Users", column="email", value=identifier)
    sql = "SELECT id FROM Posts WHERE " + entity + " = %s "
    parameters = [identifier]
    if "since" in params:
        sql += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        sql += " ORDER BY date " + params["order"]
    else:
        sql += " ORDER BY date DESC "
    if "limit" in params:
        sql += " LIMIT " + str(params["limit"])
    post_ids = dbconnector.execute_sql(sql=sql, params=parameters)
    posts_list = []
    for id in post_ids:
        id = id[0]
        posts_list.append(details(id=id, related=related))
    return posts_list


def change_deleted_status(post_id, status):
    dbconnector.exist_in_db(table="Posts", column="id", value=post_id)
    dbconnector.execute_update("UPDATE Posts SET isDeleted = %s WHERE Posts.id = %s", (status, post_id, ))
    return {
        "post": post_id
    }


def update(id, message):
    dbconnector.exist_in_db(table="Posts", column="id", value=id)
    dbconnector.execute_update('UPDATE Posts SET message = %s WHERE id = %s', (message, id, ))
    return details(id=id, related=[])


def vote(id, vote):
    dbconnector.exist_in_db(table="Posts", column="id", value=id)
    if vote == -1:
        dbconnector.execute_update("UPDATE Posts SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        dbconnector.execute_update("UPDATE Posts SET likes=likes+1, points=points+1  where id = %s", (id, ))
    return details(id=id, related=[])


def select_post(query, params):
    return dbconnector.execute_sql(query, params)


def post_query(id):
    post = select_post('SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, '
                       'isHighlighted, isSpam, likes, message, parent, points, thread, user '
                       'FROM Posts WHERE id = %s', (id, ))
    if len(post) == 0:
        return None
    return post_desc(post)

