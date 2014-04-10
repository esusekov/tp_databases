__author__ = 'egor'

import MySQLdb as db


class DBConnection:
    
    def __init__(self):
        pass

    def connect(self):
        return db.connect(self.host, self.user, self.password, self.dataBase, init_command='set names UTF8')
    host = "localhost"
    user = "root"
    password = "bugatti"
    dataBase = "db"


def execute_sql(sql, params):
    try:
        connection = DBConnection()
        connection = connection.connect()
        with connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchall()
            cursor.close()
        connection.close()
    except db.Error:
        raise db.Error("Database error.")
    return result


def execute_update(sql, params):
    try:
        connection = DBConnection()
        connection = connection.connect()
        connection.autocommit(False)
        with connection:
            cursor = connection.cursor()
            connection.begin()
            cursor.execute(sql, params)
            connection.commit()
            cursor.close()
            id = cursor.lastrowid
        connection.close()
    except db.Error:
        raise db.Error("Database error.")
    return id


def exist_in_db(table, column, value):
    if not len(execute_sql('SELECT id FROM ' + table + ' WHERE ' + column + ' = %s', (value, ))):
        raise Exception("No such element")
    return
