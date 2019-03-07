#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download video from bilibili.
"""

import sys
from selflib.download import VideoDownload
from config import parameter as param
from selflib.MySQLCommand import MySQLCommand


class Task:

    def __init__(self):
        self.list = []

    def get_list(self, path):
        with open(path, "r") as f:
            for line in f:
                self.list.append(line.strip())
        print("Get av list: {}".format(self.list))

    def set_list(self, list):
        self.list = list

    def start_download(self):
        down = VideoDownload()
        for av in self.list:
            down.get_av_number(av)
            down.set_parameter()
            down.start_download()

    def create_table(self):
        db1 = MySQLCommand(param.mysql_host, param.mysql_user, param.mysql_pass, param.mysql_database,
                           param.mysql_charset, param.mysql_table1)
        db2 = MySQLCommand(param.mysql_host, param.mysql_user, param.mysql_pass, param.mysql_database,
                           param.mysql_charset, param.mysql_table2)

        db1.create_table(param.mysql_table1, param.item_table1)
        db2.create_table(param.mysql_table2, param.item_table2)


if __name__ == "__main__":

    task = Task()

    if len(sys.argv) > 1:
        print("Get av number from shell/cmd.")
        video_list = sys.argv
        video_list.pop(0)
        task.set_list(video_list)
    else:
        print("Get av number from config file.")
        file_path = param.list_file_path
        task.get_list(file_path)

    if param.save_in_database:
        task.create_table()

    task.start_download()
