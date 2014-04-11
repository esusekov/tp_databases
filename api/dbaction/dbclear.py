__author__ = 'egor'

import MySQLdb as db

from api.dbaction import dbconnector


def clear():
    sql = ["SET foreign_key_checks = 0;",
        "truncate Followers;",
        "truncate Forums;",
        "truncate Posts;",
        "truncate Subscriptions;",
        "truncate Threads;",
        "truncate Users;",
        "SET foreign_key_checks = 1;"]
    try:
        connection = dbconnector.DBConnection()
        connection = connection.connect()
        with connection:
            cursor = connection.cursor()
            for query in sql:
                cursor.execute(query)
                connection.commit()
            cursor.close()
        connection.close()
    except db.Error:
        raise db.Error("Database error.")
    return