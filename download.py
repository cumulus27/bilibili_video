#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download video from bilibili.
"""

from BiliUtil.bili_album import Album
from BiliUtil.bili_user import User
from config import parameter as param


class VideoDownload:

    def __init__(self):
        self.av_number = None
        self.video = None

    def get_av_number(self, number):
        if "av" in number:
            number = number.replace("av", "")

        self.av_number = number
        print("Get the av number: {}".format(self.av_number))
        self.video = Album(aid=self.av_number)

    def set_parameter(self):
        self.video.set_cookie(param.cookies)

    def start_download(self):
        info = self.video.get_album_info()
        print("Start download: {}".format(info.name))

        self.video.get_album_data(base_path=param.path, name_path=True)


if __name__ == "__main__":
    av_number = "av17703354"

    down = VideoDownload()
    down.get_av_number(av_number)
    down.set_parameter()

    down.start_download()


