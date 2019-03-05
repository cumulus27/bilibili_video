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


class ScanTask:
    def __init__(self, scan_list, read_path, result_path):
        self.scan_list = scan_list
        self.read_path = read_path
        self.result_path = result_path
        self.scan_report = {}
        self.scan_result = {}
        self.finished_scan = []
        self.running_scan = {}
        self.waiting_scan = {}
        self.report_dict = {}
        self.db = None
        self.report_file = "{}Scan_Report_{}.txt"

    def set_report_name(self, name):
        self.report_file = name

    def create_report_path(self):
        # self.report_file = "{}VirusTotal_Scan_Report_{}.txt"
        time_now = time.strftime("%Y%m%d_%H%M", time.localtime(time.time()))
        self.report_file = self.report_file.format(self.result_path, time_now)
        print("The report file path is {}".format(self.report_file))
        try:
            if not os.path.exists(self.result_path):
                os.makedirs(self.result_path)
        except Exception as e:
            print("Error in create path: {}".format(e))

    def generate_report(self, lines):
        try:
            with open(self.report_file, "a+") as f:
                f.write(lines)
                f.write("\n-----------------------------------------------------------------------------------------\n")

        except Exception as e:
            print("Create result file error: {}".format(e))

    def delete_process(self):
        for i in range(len(self.finished_scan)):
            self.running_scan.pop(self.finished_scan[i])

    def generate_id(self):
        for i, scan_name in enumerate(self.scan_list):
            file_path = self.read_path + scan_name
            self.waiting_scan.update({i: file_path})
            self.scan_result.update({i: {"name": scan_name, "path": file_path, "code": None, "time": 0}})
            self.scan_report.update({i: ""})
            self.report_dict.update({i: {}})

    def check_status(self):
        self.finished_scan = []
        for key, value in self.running_scan.items():
            if not value.isAlive():
                code = value.get_result()
                # self.scan_result.update({key: {"code": code}})
                self.scan_result[key]["code"] = code
                self.finished_scan.append(key)

    def handle_scan_result(self):
        for key in self.finished_scan:
            code = self.scan_result[key]["code"]
            value = self.running_scan[key]

            self.result_operation(key, value, code)

    def result_operation(self, key, value, code):
        # If the scan exit with web error, add the scan into waiting list.
        if code >= 1 and self.scan_result[key]["time"] < param.max_retry:
            file_path = self.scan_result[key]["path"]
            self.waiting_scan.update({key: file_path})
            print("Reload the id: {}, path: {} into waiting list.".format(key, file_path))

        self.scan_result[key]["time"] += 1

        if code == 0:
            self.scan_report[key] = value.get_report_response()
            self.get_result_detail(key)

            if param.txt_report:
                lines = self.generate_normal_lines(key)
                self.generate_report(lines)
                print("Completed write reuslt into file.")

            if param.save_in_database:
                self.update_database(key)

        elif self.scan_result[key]["time"] >= param.max_retry:
            if param.txt_report:
                lines = self.generate_error_lines(key)
                self.generate_report(lines)

            if param.save_in_database:
                self.update_database(key)
        else:
            return

    def scan_loop(self, max_thread):
        while True:

            # check all the running scans, find out finished scan.
            self.check_status()
            self.handle_scan_result()
            # delete the finished scan from the running list.
            self.delete_process()

            # If the running list and waiting list all empty, all scan is finished.
            if not len(self.running_scan) and not len(self.waiting_scan):
                print("All scan task is finished.")
                print(self.scan_result)
                break

            # If the number of running scan less than max number, start new scan.
            if threading.active_count() < max_thread:

                # If there is no apk file in waiting list, skip start new scan,
                # the program will waiting the running scan finished.
                if not len(self.waiting_scan):
                    print("There is no item in the apk list, continue.")
                    print("\nThe number of active threading now: {}".format(threading.active_count()))
                    print("The active threading now:\n{}\n".format(threading.enumerate()))
                    time.sleep(5)
                    continue

                # Pop a apk file from waiting list for scan.
                thread_id, file_path = self.waiting_scan.popitem()
                print("\nStart a new thread, scan the apk: {}\n".format(file_path))

                # Start scan.
                task = self.scan_operation(file_path)
                # task.get_result()

                self.running_scan.update({thread_id: task})

            else:
                # Waiting.
                print("\nThe number of active threading now: {}".format(threading.active_count()))
                print("The active threading now:\n{}\n".format(threading.enumerate()))
                time.sleep(5)

    def generate_error_lines(self, key):
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        report_line1 = "ID: {}, Scan_date: {}, Error\n"
        report_line1 = report_line1.format(key, time_now)

        report_line2 = "Apk path: {}\n".format(self.scan_result[key]["path"])

        report_line3 = "\nError code : {},   Retry time: {}\n".format(self.scan_result[key]["code"],
                                                                      self.scan_result[key]["time"])

        lines = report_line1 + report_line2 + report_line3

        return lines

    def start_scan(self, max_thread):
        pass

    def init_database(self):
        pass

    def scan_operation(self, file_path):
        pass

    def generate_normal_lines(self, key):
        pass

    def get_result_detail(self, key):
        pass

    def update_database(self, key):
        pass


class ScanThread(threading.Thread):

    def __init__(self, read_path, result_path):
        super(ScanThread, self).__init__()
        self.read_path = read_path
        self.result_path = result_path
        self.return_code = None
        self.report_response = None

    def run(self):
        self.start_scan()

    def start_scan(self):
        pass

    def get_result(self):
        return self.return_code

    def get_report_response(self):
        return self.report_response
