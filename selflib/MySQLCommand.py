#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MySQL database command
"""
import pymysql
import re


class MySQLCommand:

    def __init__(self, host, user, password, database_name, char_set, table):
        # print("Use the MySQL database.")
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name
        self.char_set = char_set
        self.table = table

    def select_data(self, table_name, data, requirement):
        db = pymysql.connect(self.host, self.user, self.password, self.database_name, charset=self.char_set)
        results = (())
        try:
            cursor = db.cursor()
            sql = "SELECT {} FROM {} {}".format(data, table_name, requirement)
            # print(sql)
            cursor.execute(sql)
            # 提交到数据库执行
            results = cursor.fetchall()

        except Exception as e:
            print("Select data wrong: {}".format(e))
        finally:
            db.close()
            return results

    def insert_item(self, keys, values):
        db = pymysql.connect(self.host, self.user, self.password, self.database_name, charset=self.char_set)
        try:
            cursor = db.cursor()
            sql = "INSERT INTO {} ({}) VALUES ({})".format(self.table, keys, values)
            print("Insert sql: {}".format(sql))
            # print(sql)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()

        except Exception as e:
            print("Insert item wrong: {}".format(e))
        finally:
            db.close()

    def update_status(self, scid, name, status):
        db = pymysql.connect(self.host, self.user, self.password, self.database_name, charset=self.char_set)
        try:
            cursor = db.cursor()
            sql = "update {} set {}='{}' where SCID={}".format(self.table, name, status, scid)
            print("Update sql: {}".format(sql))
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()

        except Exception as e:
            print("Update status wrong: {}".format(e))
        finally:
            db.close()

    def create_table(self, table_name, parameter):
        db = pymysql.connect(self.host, self.user, self.password, self.database_name, charset=self.char_set)
        try:
            cursor = db.cursor()
            if not self.table_exists(cursor, table_name):
                print("The result table not exist, now create it.")
                sql = "CREATE TABLE {} ({})".format(table_name, parameter)
                print("SQL: {}".format(sql))
                cursor.execute(sql)
                print("Create table name : {}".format(table_name))
            else:
                print("The table named {} is exited, can not recreate it!!!".format(table_name))

        except Exception as e:
            print("Creating database wrong: {}".format(e))
        finally:
            db.close()

    @staticmethod
    def table_exists(con, table_name):
        sql = "show tables;"
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        print("Tables in database: {}".format(table_list))
        if table_name.lower() in table_list:
            return True
        else:
            return False


if __name__ == "__main__":
    # database = MySQLCommand()
    # database.create_if_not_exist()
    pass
