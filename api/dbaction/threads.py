__author__ = 'egor'

from api.dbaction import users, forums, dbconnector


def details(id, related):
    thread = dbconnector.execute_sql(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (id, )
    )
    if len(thread) == 0:
        raise Exception('No such thread')
    thread = thread_desc(thread)

    if "user" in related:
        thread["user"] = users.details(thread["user"])
    if "forum" in related:
        thread["forum"] = forums.forum_details(short_name=thread["forum"], related=[])

    return thread


def thread_desc(thread):
    thread = thread[0]
    response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }
    return response


def save_thread(forum, title, isClosed, user, date, message, slug, optional):
    dbconnector.exist_in_db(table="Users", column="email", value=user)
    dbconnector.exist_in_db(table="Forums", column="short_name", value=forum)

    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    thread = dbconnector.execute_sql(
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE slug = %s', (slug, )
    )
    if len(thread) == 0:
        dbconnector.execute_update(
            'INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (forum, title, isClosed, user, date, message, slug, isDeleted, )
        )
        thread = dbconnector.execute_sql(
            'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
            'FROM Threads WHERE slug = %s', (slug, )
        )
    response = thread_desc(thread)

    del response["dislikes"]
    del response["likes"]
    del response["points"]
    del response["posts"]

    return response



def vote(id, vote):
    dbconnector.exist_in_db(table="Threads", column="id", value=id)

    if vote == -1:
        dbconnector.execute_update("UPDATE Threads SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        dbconnector.execute_update("UPDATE Threads SET likes=likes+1, points=points+1  where id = %s", (id, ))

    return details(id=id, related=[])


def change_closed_status(id, isClosed):
    dbconnector.exist_in_db(table="Threads", column="id", value=id)
    dbconnector.execute_update("UPDATE Threads SET isClosed = %s WHERE id = %s", (isClosed, id, ))

    response = {
        "thread": id
    }

    return response


def update_thread(id, slug, message):
    dbconnector.exist_in_db(table="Threads", column="id", value=id)
    dbconnector.execute_update('UPDATE Threads SET slug = %s, message = %s WHERE id = %s',
                          (slug, message, id, ))

    return details(id=id, related=[])


def list_of_threads(entity, identificator, related, params):
    if entity == "forum":
        dbconnector.exist_in_db(table="Forums", column="short_name", value=identificator)
    if entity == "user":
        dbconnector.exist_in_db(table="Users", column="email", value=identificator)
    sql = "SELECT id FROM Threads WHERE " + entity + " = %s "
    parameters = [identificator]

    if "since" in params:
        sql += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        sql += " ORDER BY date " + params["order"]
    else:
        sql += " ORDER BY date DESC "
    if "limit" in params:
        sql += " LIMIT " + str(params["limit"])

    thread_ids = dbconnector.execute_sql(sql=sql, params=parameters)
    threads_list = []

    for id in thread_ids:
        id = id[0]
        threads_list.append(details(id=id, related=related))

    return threads_list


def change_deleted_status(thread_id, status):
    dbconnector.exist_in_db(table="Threads", column="id", value=thread_id)
    dbconnector.execute_update("UPDATE Threads SET isDeleted = %s WHERE id = %s", (status, thread_id, ))

    response = {
        "thread": thread_id
    }
    return response
