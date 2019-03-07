#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some tools by py.
"""

import os
import time
import json
import threading

import config.parameter as param


class LoopTask:
    def __init__(self):
        self.task_result = {}
        self.finished_task = []
        self.running_task = {}
        self.waiting_task = {}
        self.max_id = 0
        self.db = None

    def delete_process(self):
        for i in range(len(self.finished_task)):
            self.running_task.pop(self.finished_task[i])

    def check_status(self):
        self.finished_task = []
        for key, value in self.running_task.items():
            if not value.isAlive():
                code = value.get_result()
                self.task_result[key]["code"] = code
                self.finished_task.append(key)

    def handle_task_result(self):
        for key in self.finished_task:
            self.result_operation(key)

    def result_operation(self, key):
        pass

    def scan_loop(self, max_thread):
        
        while True:

            self.loop_prepare()

            # check all the running task, find out finished task.
            self.check_status()
            self.handle_task_result()
            # delete the finished task from the running list.
            self.delete_process()

            # If the number of running scan less than max number, start new task.
            if threading.active_count() < max_thread:
                # If there is no task in waiting list, skip start new task,
                # the program will waiting the running scan finished.
                if not len(self.waiting_task):
                    print("There is no task in queue list, continue.")
                    print("\nThe number of active threading now: {}".format(threading.active_count()))
                    print("The active threading now:\n{}\n".format(threading.enumerate()))
                    time.sleep(5)
                    continue

                # Pop a task from waiting list for scan.
                thread_id, one_task = self.waiting_task.popitem()
                print("\nStart a new thread: {}\n".format(one_task))

                # Start scan.
                task = self.scan_operation(one_task)
                # task.get_result()

                self.running_task.update({thread_id: task})

            else:
                # Waiting.
                print("\nThe number of active threading now: {}".format(threading.active_count()))
                print("The active threading now:\n{}\n".format(threading.enumerate()))
                time.sleep(5)

    def start_scan(self, max_thread):
        pass

    def init_database(self):
        pass

    def scan_operation(self, one_task):
        pass

    def loop_prepare(self):
        pass


class ThreadTask(threading.Thread):

    def __init__(self):
        super(ThreadTask, self).__init__()
        self.return_code = None
        self.response = None

    def run(self):
        self.start_scan()

    def start_scan(self):
        pass

    def get_result(self):
        return self.return_code

    def get_report_response(self):
        return self.response
