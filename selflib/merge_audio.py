#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Merge the video and the acc.
"""

import os
import time
import subprocess
from config import parameter as param
from selflib.tools import *
from selflib.MySQLCommand import MySQLCommand


class Merge:
    def __init__(self):
        pass

    @classmethod
    def merge_video_file(cls, path, delete=False, cid=None):
        """
               Disassembles a given offset in the DEX file

               :param path: offset to disassemble in the file (from the beginning of the file)
               :type path: str
               :param delete:
               :type delete: bool
               :param cid:
               :type cid: str
               """
        # 完成目录下flv视频文件与aac音频文件的合并
        if os.path.exists(path) and os.path.isdir(path):
            path = os.path.abspath(path)  # 将路径替换为绝对路径
            file_list = os.listdir(path)  # 获取路径下文件列表
            for file in file_list:
                # file_path = path + '\\' + file
                file_path = os.path.join(path, file)
                file_name = os.path.splitext(file)[0]
                prefix, suffix = os.path.splitext(file_path)
                if suffix == '.flv':
                    if os.path.exists(prefix + '.mp4'):
                        print_1('视频', end='')
                        print_cyan(file_name, end='')
                        print_1('已找到，跳过该文件')
                        return

                    if os.path.exists(prefix + '.aac'):
                        print_b('已找到未合并文件{}，正在合并'.format(file_name))
                        shell = 'ffmpeg -i "{}.flv" -i "{}.aac" -c copy -f mp4 -y "{}.mp4"'
                        command = shell.format(prefix, prefix, prefix)
                        print("Shell command:\n{}\n".format(command))
                        process = subprocess.Popen(command,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   shell=True)
                        print("Start merge ...\n")
                        cls.wait_and_print(process)
                        # process.communicate()

                        if os.path.exists(prefix + '.mp4'):
                            print_1('视频', end='')
                            print_cyan(file_name, end='')
                            print_1('已经', end='')
                            print_g('完成合并', end='')
                            if delete:
                                os.remove(prefix + '.flv')
                                os.remove(prefix + '.aac')
                                print_1('，原始音视频', end='')
                                print_r('已删除')

                                if param.merge_audio_delete:
                                    cls.update_database(cid, "piece_delete", 1)
                            else:
                                print_1('，原始音视频', end='')
                                print_y('未删除')

                            if param.save_in_database:
                                cls.update_database(cid, "audio_merge", 1)
                        else:
                            raise BaseException('视频与音频合并失败，不知道发生了什么')
                    else:
                        raise BaseException('未找到与视频匹配的音频!!!')
                elif suffix == '.mp4':
                    print_1('视频', end='')
                    print_cyan(file_name, end='')
                    print_1('已找到，跳过该文件')
        else:
            raise BaseException('输入的文件夹路径不存在')

    @classmethod
    def wait_and_print(cls, p):
        while True:
            line = p.stderr.readline()
            while line:
                line = line.decode("utf8")
                line = line.strip()
                print(line)
                line = p.stderr.readline()

            if p.poll() != None:
                break
            time.sleep(2)

    @classmethod
    def update_database(cls, cid, merge_type, value):
        db2 = MySQLCommand(param.mysql_host, param.mysql_user, param.mysql_pass, param.mysql_database,
                           param.mysql_charset, param.mysql_table2)

        time_now = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
        line = "{} = '{}', merge_time = '{}'"
        line = line.format(merge_type, value, time_now)
        cid = cid.replace("cv", "")
        db2.update_items("cid", cid, line)


if __name__ == "__main__":

    file_path = "D:\Code\github\Private\merge_test"

    Merge.merge_video_file(file_path)



