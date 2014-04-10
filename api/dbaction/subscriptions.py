__author__ = 'egor'

import api.dbaction.dbconnector as dbconnector


def add_subscription(email, thread_id):
    dbconnector.exist_in_db(table="Threads", column="id", value=thread_id)
    dbconnector.exist_in_db(table="Users", column="email", value=email)
    subscription = dbconnector.execute_sql(
        'SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscription) == 0:
        dbconnector.execute_update(
            'INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread_id, email, )
        )
        subscription = dbconnector.execute_sql(
            'SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
        )

    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response


def delete_subscription(email, thread_id):
    dbconnector.exist_in_db(table="Threads", column="id", value=thread_id)
    dbconnector.exist_in_db(table="Users", column="email", value=email)
    subscription = dbconnector.execute_sql(
        'SELECT thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )
    if len(subscription) == 0:
        raise Exception("user " + email + " does not subscribe thread #" + str(thread_id))
    dbconnector.execute_update(
        'DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (email, thread_id, )
    )

    response = {
        "thread": subscription[0][0],
        "user": subscription[0][1]
    }
    return response
