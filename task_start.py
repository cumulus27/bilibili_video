#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download video from bilibili.
"""

from selflib.task import ThreadTask
from selflib.task import LoopTask
from selflib.download import VideoDownload
from selflib.MySQLCommand import MySQLCommand

import config.parameter as param


class BiliVideoThread(ThreadTask):

    def __init__(self, aid):
        super(BiliVideoThread, self).__init__()
        self.aid = aid

    def start_scan(self):
        down = VideoDownload()

        down.get_av_number(self.aid)
        down.set_parameter()
        down.start_download()

        self.return_code = 0


class BiliVideoTask(LoopTask):

    def __init__(self):
        super(BiliVideoTask, self).__init__()
        self.list = []

    def start_scan(self, max_thread):

        if param.from_txt:
            self.get_list_from_file(param.list_file_path)
            for aid in self.list:
                self.max_id += 1
                self.waiting_task.update({self.max_id: aid})

        if param.save_in_database:
            self.init_database()
            self.db.create_table(param.mysql_table1, param.item_table1)
            self.db.create_table(param.mysql_table2, param.item_table2)

        self.scan_loop(max_thread)

    def loop_prepare(self):
        if param.from_database:
            self.get_aid_from_database()

    def init_database(self):
        self.db = MySQLCommand(param.mysql_host, param.mysql_user, param.mysql_pass, param.mysql_database,
                               param.mysql_charset, param.mysql_table1)

    def scan_operation(self, aid):
        task = BiliVideoThread(aid)
        task.start()

        return task

    def handle_scan_result(self):
        pass

    def get_list_from_file(self, path):
        try:
            with open(path, "r") as f:
                for line in f:
                    self.list.append(line.strip())
            print("Get aid list: {}".format(self.list))

        except FileNotFoundError as e:
            print("The file not exist: {}".format(e))
            raise

    def get_aid_from_database(self):

        table_name = param.mysql_table1
        data = "aid"
        requirement = "WHERE download=0 ORDER BY METHOD DESC, insert_time limit 1"

        results = self.db.select_data(table_name, data, requirement)
        if len(results) > 1:
            print("The get one function get {} results! Something wrong!".format(len(results)))
            return

        get_aid = results[0][0]

        self.waiting_task.update({self.max_id: get_aid})


if __name__ == "__main__":

    task = BiliVideoTask()

    max_task = param.max_thread
    task.start_scan(max_task)
