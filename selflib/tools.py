#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some static function.
"""

import os
import time

import config.parameter as param


def print_0(message, end='\n'):
    print('\033[0;30;0m{}\033[0m'.format(str(message)), end=end)


def print_1(message, end='\n'):
    print('\033[0;37;0m{}\033[0m'.format(str(message)), end=end)


def print_r(message, end='\n'):
    print('\033[0;31;0m{}\033[0m'.format(str(message)), end=end)


def print_g(message, end='\n'):
    print('\033[0;32;0m{}\033[0m'.format(str(message)), end=end)


def print_y(message, end='\n'):
    print('\033[0;33;0m{}\033[0m'.format(str(message)), end=end)


def print_b(message, end='\n'):
    print('\033[0;34;0m{}\033[0m'.format(str(message)), end=end)


def print_cyan(message, end='\n'):
    # 青色
    print('\033[0;36;0m{}\033[0m'.format(str(message)), end=end)


def print_gray(message, end='\n'):
    # 灰色
    print('\033[0;37;0m{}\033[0m'.format(str(message)), end=end)


class Tools:

    def __init__(self):
        pass

    @classmethod
    def get_time_stamp(cls):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y%m%d%H%M%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        data_tail = "%03d" % data_secs
        # data_secs = str(data_secs).split(".")[0]
        stamp = data_head + data_tail
        return stamp

    @staticmethod
    def get_file_list(file_path):

        file_list = []

        try:
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    for file_type in param.file_types:
                        if file.endswith(file_type):
                            file_list.append(file)

        except Exception as e:
            print("Read file error: {}".format(e))

        return file_list
