#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Merge the fragment videos.
"""

import os
import subprocess
from moviepy.editor import *

from selflib.tools import *
import config.parameter as param


class FragmentMerge:

    def __init__(self):
        pass

    @classmethod
    def merge_fragment(cls, movie_list, file_name, delete):
        """
            合并视频的方法
            @movie_list 按顺序排好的需要合并的视频
            @des 存储目标路径
        """
        L = []
        for movie in movie_list:
            if os.path.splitext(movie)[1] == '.flv':
                video = VideoFileClip(movie)
                L.append(video)
            else:
                print("{}不是.flv文件".format(movie))
                return
        if len(L) == 0:
            return
        # 拼接视频
        final_clip = concatenate_videoclips(L)
        # Generate new file name.
        out_name = cls.get_output_file_name(file_name)
        print("Merge the files to {}".format(out_name))

        sep = os.path.sep
        base_paths = movie_list[0].split(sep).pop()
        base_path = sep.join(base_paths)
        prefix = os.path.join(base_path, out_name)

        # 生成目标视频文件
        final_clip.to_videofile(prefix, fps=24, remove_temp=False)

        if os.path.exists(prefix):
            print_1('视频', end='')
            print_cyan(file_name, end='')
            print_1('已经', end='')
            print_g('完成合并', end='')
            if delete:
                for flv_file in movie_list:
                    os.remove(flv_file)
                print_1('，原始音视频', end='')
                print_r('已删除')
            else:
                print_1('，原始音视频', end='')
                print_y('未删除')

    @classmethod
    def merge_fragment_ffmpeg(cls, flv_list, file_name, delete):
        return_code = cls.write_list_in_file(flv_list)
        if return_code == 1:
            return

        if os.path.exists(param.merge_fragment_files_path):
            print_b('Find the files list, start to merge {}.'.format(file_name))
            shell = "ffmpeg -f concat -safe 0 -i {} -c copy {}"
            out_name = cls.get_output_file_name(file_name)
            prefix = cls.get_output_file_path(flv_list, out_name)
            list_path = os.path.abspath(param.merge_fragment_files_path)
            command = shell.format(list_path, prefix)
            print("Shell command:\n{}\n".format(command))
            # log_file = open(file_path + param.merge_log_path, 'w+')
            process = subprocess.Popen(command,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            print("Start merge ...\n")
            # process.communicate()
            cls.wait_and_print(process)

            if os.path.exists(prefix):
                print_1('视频', end='')
                print_cyan(file_name, end='')
                print_1('已经', end='')
                print_g('完成合并', end='')
                if delete:
                    for flv_file in flv_list:
                        os.remove(flv_file)
                    print_1('，原始音视频', end='')
                    print_r('已删除')
                else:
                    print_1('，原始音视频', end='')
                    print_y('未删除')
            else:
                raise BaseException("Fail to merge.")
        else:
            raise BaseException("Not find the file list for merge.")

    @classmethod
    def get_output_file_name(cls, file_name):
        print("Get the example file name: {}".format(file_name))
        names = file_name.split("_")
        names.pop()
        out_name = "_".join(names) + ".mp4"
        print("Merge the fragments to {}".format(out_name))

        return out_name

    @classmethod
    def get_output_file_path(cls, flv_list, out_name):
        sep = os.path.sep
        base_paths = flv_list[0].split(sep)
        base_paths.pop()
        base_path = sep.join(base_paths)
        prefix = os.path.join(base_path, out_name)
        print("Output file path is:\n{}".format(prefix))

        return prefix

    @classmethod
    def write_list_in_file(cls, flv_list):
        try:
            with open(param.merge_fragment_files_path, "wb") as f:
                for file in flv_list:
                    file = "file " + file + "\n"
                    file = file.replace("\\", "\\\\")
                    f.write(file.encode("utf8"))

            return 0
        except Exception as e:
            print("There is something wrong: {}".format(e))
            return 1

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
    def start_merge(cls, path, delete=False):
        if os.path.exists(path) and os.path.isdir(path):
            path = os.path.abspath(path)  # 将路径替换为绝对路径
            sub_dir_list = os.listdir(path)  # 获取路径下文件夹列表.
            for sub_dir in sub_dir_list:
                sub_path = os.path.join(path, sub_dir)
                if os.path.exists(sub_path) and os.path.isdir(sub_path):
                    file_list = os.listdir(sub_path)

                    flv_list = []
                    file_name_example = ""
                    for file in file_list:
                        file_path = os.path.join(sub_path, file)
                        file_name = os.path.splitext(file)[0]
                        print("Find file: {}".format(file))
                        prefix, suffix = os.path.splitext(file_path)
                        if suffix == '.flv':
                            flv_list.append(file_path)
                            file_name_example = file_name

                        elif suffix == '.mp4':
                            print_1('视频', end='')
                            print_cyan(file_name, end='')
                            print_1('已找到，跳过该文件')
                            return

                    print("The file list:\n{}".format(flv_list))

                    if param.use_ffmpeg_to_merge_fragments:
                        print("Use ffmpeg to merge.")
                        cls.merge_fragment_ffmpeg(flv_list, file_name_example, delete)
                    else:
                        print("Use moviepy to merge.")
                        cls.merge_fragment(flv_list, file_name_example, delete)
        else:
            raise BaseException("No such a direction:\n{}".format(path))
