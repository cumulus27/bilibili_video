#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download video from bilibili.
"""

from selflib.download import VideoDownload
from config import parameter as param


class Task:

    def __init__(self):
        self.list = []

    def get_list(self, path):
        with open(path, "r") as f:
            for line in f:
                self.list.append(line.strip())
        print("Get av list: {}".format(self.list))

    def start_download(self):
        down = VideoDownload()
        for av in self.list:
            down.get_av_number(av)
            down.set_parameter()
            down.start_download()


if __name__ == "__main__":

    file_path = param.list_file_path

    task = Task()
    task.get_list(file_path)

    task.start_download()