#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Insert the av number to database from file.
"""

from selflib.MySQLCommand import MySQLCommand
import config.parameter as param


def insert_start():

    file_path = param.list_file_path
    db1 = MySQLCommand(param.mysql_host, param.mysql_user, param.mysql_pass, param.mysql_database,
                      param.mysql_charset, param.mysql_table1)
    db2 = MySQLCommand(param.mysql_host, param.mysql_user, param.mysql_pass, param.mysql_database,
                      param.mysql_charset, param.mysql_table2)

    db1.create_table(param.mysql_table1, param.item_table1)
    db2.create_table(param.mysql_table2, param.item_table2)

    try:
        with open(file_path, "r") as f:
            line = f.readline()
            while line:
                db1.insert_item("av", line.strip())
                db2.insert_item("av", line.strip())
                line = f.readline()

    except FileNotFoundError as e:
        print("File not find: {}".format(file_path))
        print(e)

    except Exception as e:
        raise UserWarning


if __name__ == "__main__":

    insert_start()
