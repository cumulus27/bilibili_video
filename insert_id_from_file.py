#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Insert the av number to database from file.
"""

import time
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
                time_now = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
                db1.insert_item("aid, insert_time, download", "'{}', '{}', 0".format(line.strip(), time_now))
                # db2.insert_item("aid, insert_time, download", "'{}', '{}', 0".format(line.strip(), time_now))
                line = f.readline()

    except FileNotFoundError as e:
        print("File not find: {}".format(file_path))
        print(e)

    except Exception as e:
        raise UserWarning


if __name__ == "__main__":

    insert_start()
