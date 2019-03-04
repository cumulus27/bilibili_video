#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Merge the video and the acc.
"""

import os
import subprocess
import BiliUtil
from config import parameter as param
from selflib.merge_audio import Merge


class MergeTask:
    def __init__(self):
        self.list = []

    def get_list(self, path):
        with open(path, "rb") as f:
            for line in f:
                line = line.decode("utf8")
                self.list.append(line.strip())
        print("Get merge list: {}".format(self.list))

    def start_merge(self):
        for path in self.list:
            Merge.merge_video_file(path, delete=False)


if __name__ == "__main__":

    file_path = param.merge_audio_path

    merge = MergeTask()
    merge.get_list(file_path)

    merge.start_merge()
