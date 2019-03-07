import os
import re
import json
import time
import requests
from urllib import parse

import BiliUtil.static_value as v
import BiliUtil.static_func as f
from BiliUtil.bili_video import Video

from selflib.MySQLCommand import MySQLCommand
import config.parameter as parameter


class Album:
    cookie = None

    aid = None

    name = None
    time = None
    desc = None
    zone = None
    num = None
    cover = None
    like = None
    coin = None
    favorite = None
    share = None
    view = None
    danmu = None
    video_list = list()

    raw_json_data = None
    cache_path = None

    def __init__(self, aid=None):
        self.aid = aid

    def set_album(self, aid=None):
        self.aid = aid
        self.name = None
        self.time = None
        self.desc = None
        self.zone = None
        self.num = None
        self.cover = None
        self.like = None
        self.coin = None
        self.favorite = None
        self.share = None
        self.view = None
        self.danmu = None
        self.owner = None
        self.dynamic = None
        self.video_list = list()

    def set_by_url(self, url):
        input_url = parse.urlparse(url)
        aid = re.match('/video/av([0-9]+)', input_url.path).group(1)
        self.set_album(aid)

    def set_cookie(self, cookie):
        self.cookie = cookie
        for video in self.video_list:
            video.set_cookie(cookie)

    def get_album_info(self):
        if self.aid is None:
            raise BaseException('缺少必要的参数')

        f.print_1('正在获取视频信息...', end='')
        param = {
            'aid': str(self.aid)
        }
        http_result = requests.get(v.URL_UP_ALBUM, params=param,
                                   headers=f.new_http_header(v.URL_UP_ALBUM))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        # 修改对象信息
        self.aid = json_data['data']['aid']
        self.time = json_data['data']['ctime']
        self.desc = json_data['data']['desc']
        self.name = json_data['data']['title']
        self.zone = json_data['data']['tname']
        self.num = json_data['data']['videos']
        self.cover = json_data['data']['pic']
        self.like = json_data['data']['stat']['like']
        self.coin = json_data['data']['stat']['coin']
        self.favorite = json_data['data']['stat']['favorite']
        self.share = json_data['data']['stat']['share']
        self.view = json_data['data']['stat']['view']
        self.danmu = json_data['data']['stat']['danmaku']
        self.owner = json_data['data']['owner']['name']
        self.dynamic = json_data['data']['dynamic']
        self.video_list = list()

        for page in json_data['data']['pages']:
            cv = Video(self.aid, page['cid'], page['page'], page['part'])
            cv.set_cookie(self.cookie)
            self.video_list.append(cv)

        self.raw_json_data = json_data

        if parameter.save_in_database:
            self.insert_into_database()

        return self

    def get_album_data(self, base_path='', name_path=False, max_length=None):
        if len(self.video_list) == 0:
            self.get_album_info()

        base_path = os.path.abspath(base_path)  # 获取绝对路径地址
        if name_path:
            # 检查路径名中的特殊字符
            temp_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s'‘’]", '_', self.name)
            if len(temp_name) == 0:
                temp_name = self.aid
            cache_path = base_path + '/{}'.format(temp_name)
        else:
            cache_path = base_path + '/{}'.format(self.aid)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self.cache_path = cache_path

        f.print_1('正在获取视频封面--', end='')
        f.print_b('av:{}'.format(self.aid))
        http_result = requests.get(self.cover)
        with open(cache_path + '/cover.jpg', 'wb') as file:
            file.write(http_result.content)
        f.print_g('[OK]', end='')
        f.print_1('视频封面已保存')

        for video in self.video_list:
            video.get_video_data(cache_path, name_path, max_length)

        with open(cache_path + '/info.json', 'w', encoding="utf8") as file:
            json_info = json.dumps(self.get_dict_info(), ensure_ascii=False,
                                   sort_keys=True, indent=4, separators=(',', ': '))
            # print(type(json_info))
            # print(json_info)
            file.write(json_info)

        self.write_raw_json()
        if parameter.save_in_database:
            self.update_download_status(0)

    def get_dict_info(self):
        json_data = vars(self).copy()
        video_list = []
        if 'video_list' in json_data:
            for video in json_data['video_list']:
                video_list.append(video.get_dict_info())
            json_data['video_list'] = video_list
            # print(type(json_data["name"]))
            # print(json_data["name"])
        return json_data

    def write_raw_json(self):
        with open(self.cache_path + '/raw_info.json', 'w', encoding="utf8") as file:
            json_info = json.dumps(self.raw_json_data, ensure_ascii=False,
                                   sort_keys=True, indent=4, separators=(',', ': '))
            file.write(json_info)

    # TODO(py) Test this function. Fix the bug of " '" in value.
    def insert_into_database(self):
        db1 = MySQLCommand(parameter.mysql_host, parameter.mysql_user, parameter.mysql_pass, parameter.mysql_database,
                           parameter.mysql_charset, parameter.mysql_table1)

        aid = db1.select_data(parameter.mysql_table1, "aid", "where aid = {}".format(self.aid))
        up_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(self.time))
        if aid:
            print("The aid is already in the database, update.")
            line = "title = '{}', videos = '{}', owner = '{}', tname = '{}'," \
                   " dynamic = '{}', detail = '{}', ctime = '{}', download = '{}'"
            line = line.format(self.name.replace("'", "\\'"), self.num,
                               self.owner.replace("'", "\\'"), self.zone,
                               self.dynamic, self.desc.replace("'", "\\'"), up_time, 1)
            db1.update_items("aid", self.aid, line)
        else:
            print("The aid is not in the database, create.")
            time_now = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
            key = "aid, title, videos, owner, tname, dynamic, detail," \
                  "ctime, insert_time, download"
            line = "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'"
            line = line.format(self.aid, self.name.replace("'", "\\'"), self.num,
                               self.owner.replace("'", "\\'"), self.zone,
                               self.dynamic, self.desc.replace("'", "\\'"), up_time, time_now, 0)
            db1.insert_item(key, line)

    def update_download_status(self, exit_code):
        db1 = MySQLCommand(parameter.mysql_host, parameter.mysql_user, parameter.mysql_pass, parameter.mysql_database,
                           parameter.mysql_charset, parameter.mysql_table1)

        line = "download = '{}', exit_code = '{}' "
        line = line.format(1, exit_code)
        db1.update_items("aid", self.aid, line)
