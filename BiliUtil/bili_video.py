import os
import re
import json
import time
import requests
import subprocess

import BiliUtil.static_value as v
import BiliUtil.static_func as f
from selflib.merge_audio import Merge
from selflib.merge_piece import PieceMerge

import config.parameter as parameter
from selflib.MySQLCommand import MySQLCommand


class Video:
    cookie = None

    aid = None
    cid = None
    index = None  # Page index 分P下标
    name = None  # Page name 分P名称

    quality = None
    quality_des = None
    length = None
    video = None
    audio = None
    format = None

    raw_json_data = None
    cache_path = None

    def __init__(self, aid=None, cid=None, index=None, name=None):
        self.aid = aid
        self.cid = cid
        self.index = index
        self.name = name

    def set_video(self, aid=None, cid=None, index=None, name=None):
        self.aid = aid
        self.cid = cid
        self.index = index
        self.name = name
        self.quality = None
        self.length = None
        self.video = None
        self.audio = None
        self.format = None

    def set_cookie(self, cookie):
        if isinstance(cookie, dict):
            self.cookie = {
                'SESSDATA': cookie['SESSDATA']
            }
        elif isinstance(cookie, str) and len(cookie) > 0:
            for line in cookie.split(';'):
                name, value = line.strip().split('=', 1)
                if name == 'SESSDATA':
                    self.cookie = {
                        'SESSDATA': value
                    }
                    break
        else:
            self.cookie = dict()

    def get_video_info(self, qn=116):
        if self.aid is None or self.cid is None:
            raise BaseException('缺少必要的参数')

        f.print_1('正在获取分P信息...', end='')
        param = {
            'avid': str(self.aid),
            'cid': str(self.cid),
            'qn': qn,  # 默认使用最高画质下载
            'otype': 'json',
            'fnver': 0,
            'fnval': 16
        }
        http_result = requests.get(v.URL_UP_VIDEO, params=param, cookies=self.cookie,
                                   headers=f.new_http_header(v.URL_UP_INFO))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        # 自动识别不同的数据来源
        if 'dash' in json_data['data']:
            self.quality = json_data['data']['quality']
            self.length = json_data['data']['timelength']
            self.video = json_data['data']['dash']['video'][-1]['baseUrl']
            self.audio = json_data['data']['dash']['audio'][0]['baseUrl']
        elif 'durl' in json_data['data']:
            self.quality = json_data['data']['quality']
            self.length = json_data['data']['timelength']
            # self.video = json_data['data']['durl'][-1]['url']
            self.get_full_url_list(json_data)

        for index, val in enumerate(json_data['data']['accept_quality']):
            if val == self.quality:
                self.quality_des = json_data['data']['accept_description'][index]
                break

        self.format = json_data['data']['format']

        self.raw_json_data = json_data
        self.quality_des = self.quality_des.replace(" ", "")

        return self

    def get_video_data(self, base_path='', name_path=False, max_length=None):
        if self.video is None and self.audio is None:
            self.get_video_info()

        if max_length is not None and max_length < self.length:
            f.print_y('视频：{}，超出限定长度取消下载')
            return

        base_path = os.path.abspath(base_path)  # 获取绝对路径地址
        if name_path:
            # 检查路径名中的特殊字符
            temp_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s'‘’]", '_', self.name)
            temp_name = re.sub(r'[‘’]', '_', temp_name)
            if len(temp_name) == 0:
                temp_name = "cv" + str(self.cid)
            # cache_path = base_path + '/{}'.format(temp_name)
            cache_path = os.path.join(base_path, temp_name)
        else:
            # cache_path = base_path + '/{}'.format(self.cid)
            cache_path = os.path.join(base_path,"cv" + str(self.cid))
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self.cache_path = cache_path

        if parameter.save_in_database:
            self.insert_into_database()

        # 使用两个进程分别下载视频和音频
        f.print_1('正在下载视频和配套音--', end='')
        f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
        self.cid = "cv" + str(self.cid)
        if self.audio is not None and self.video is not None:
            self.aria2c_download(cache_path, '{}_{}.aac'.format(self.cid, self.quality_des), self.audio)
            self.aria2c_download(cache_path, '{}_{}.flv'.format(self.cid, self.quality_des), self.video)
            self.write_audio_file(cache_path)
            if parameter.save_in_database:
                self.update_status("audio_merge", 0)
                self.update_status("merge_type", 1)

            if parameter.auto_merge:
                merge = Merge()
                merge.merge_video_file(cache_path, delete=parameter.merge_audio_delete, cid=self.cid)

        if self.video is not None and self.audio is None:
            # self.aria2c_download(cache_path, '{}_{}.mp4'.format(self.cid, self.quality_des), self.video)
            self.download_full_list(cache_path)
        else:
            f.print_y('无需独立下载音频')
        f.print_cyan('==============================================================')

        json_path = os.path.join(cache_path, "info.json")
        with open(json_path, 'w', encoding='utf8') as file:
            file.write(str(json.dumps(self.get_dict_info(), ensure_ascii=False,
                                      sort_keys=True, indent=4, separators=(',', ': '))))

        self.write_raw_json()

    def aria2c_download(self, cache_path, file_name, download_url):
        referer = 'https://www.bilibili.com/video/av' + str(self.aid)
        shell = 'aria2c -c -s 1 -d "{}" -o "{}" --referer="{}" "{}"'
        shell = shell.format(cache_path, file_name, referer, download_url)
        print("Download command:\n{}\n".format(shell))
        process = subprocess.Popen(shell, shell=True)
        process.wait()

        file_path = '{}/{}'.format(cache_path, file_name)
        if os.path.exists(file_path):
            f.print_g('[OK]', end='')
            f.print_1('文件{}下载成功--'.format(file_name), end='')
            f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
        else:
            f.print_r('[ERR]', end='')
            f.print_1('文件{}下载失败--'.format(file_name), end='')
            f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
            f.print_r(shell.format(file_path, referer, download_url))
            raise BaseException('av:{},cv:{},下载失败'.format(self.aid, self.cid))

    def get_dict_info(self):
        json_data = vars(self).copy()
        return json_data

    def write_raw_json(self):
        json_path = os.path.join(self.cache_path, "raw_info.json")
        with open(json_path, 'w', encoding="utf8") as file:
            json_info = json.dumps(self.raw_json_data, ensure_ascii=False,
                                   sort_keys=True, indent=4, separators=(',', ': '))
            file.write(json_info)

    def get_full_url_list(self, data):

        url_list = []
        for piece in data['data']['durl']:
            url_list.append((piece["order"], piece["url"]))

        self.video = url_list

    def download_full_list(self, cache_path):

        if len(self.video) > 1:
            for order, url in self.video:
                file_name = "%s_%s_%03d.flv" % (self.cid, self.quality_des, int(order))
                print("Download {}".format(file_name))
                self.aria2c_download(cache_path, file_name, url)

            self.write_piece_file(cache_path)
            if parameter.save_in_database:
                self.update_status("piece_merge", 0)
                self.update_status("merge_type", 2)

            if parameter.auto_merge:
                merge = PieceMerge()
                merge.start_merge(cache_path, delete=parameter.merge_piece_delete, cid=self.cid)

        else:
            print("There is only one piece.")
            url = self.video[0][1]
            self.aria2c_download(cache_path, '{}_{}.mp4'.format(self.cid, self.quality_des), url)

            if parameter.save_in_database:
                self.update_status("merge_type", 0)

    @classmethod
    def write_piece_file(cls, cache_path):
        cache_path += "\n"
        try:
            with open(parameter.merge_piece_path, "ab+") as f:
                f.write(cache_path.encode("utf8"))
        except Exception as e:
            print("There is something wrong: {}".format(e))

    @classmethod
    def write_audio_file(cls, cache_path):
        cache_path += "\n"
        try:
            with open(parameter.merge_audio_path, "ab+") as f:
                f.write(cache_path.encode("utf8"))
        except Exception as e:
            print("There is something wrong: {}".format(e))

    # TODO(py) Test this function.
    def insert_into_database(self):
        db2 = MySQLCommand(parameter.mysql_host, parameter.mysql_user, parameter.mysql_pass, parameter.mysql_database,
                           parameter.mysql_charset, parameter.mysql_table2)

        time_now = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
        length_s = int(self.length) / 1000
        m, s = divmod(length_s, 60)
        length_m = "%d:%02d" % (m, s)
        cache_path = self.cache_path.replace("\\", "\\\\")

        key = "cid, aid, quality, title, length, path, quality_des, format," \
              " download_time, audio_merge, piece_merge, piece_delete"
        line = "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'"
        line = line.format(self.cid, self.aid, self.quality, self.name.replace("'", "\\'")
                           , length_m, cache_path.replace("'", "\\'"),
                           self.quality_des, self.format, time_now, 1, 1, 0)
        db2.insert_item(key, line)

    def update_status(self, merge_type, value):
        db2 = MySQLCommand(parameter.mysql_host, parameter.mysql_user, parameter.mysql_pass, parameter.mysql_database,
                           parameter.mysql_charset, parameter.mysql_table2)

        line = "{} = '{}', exit_code = '{}'"
        line = line.format(merge_type, value, 0)
        cid = self.cid.replace("cv", "")
        db2.update_items("cid", cid, line)
