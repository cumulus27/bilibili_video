#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Merge the fragment videos.
"""

from moviepy.editor import *
import os

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
                print('%s 不是.flv文件' % movie)
                return
        if len(L) == 0:
            return
        # 拼接视频
        final_clip = concatenate_videoclips(L)

        # generate new file name.
        names = file_name.split("_")
        names.pop()
        out_name = "_".join(names) + ".mp4"

        # 生成目标视频文件
        final_clip.to_videofile(out_name, fps=24, remove_temp=False)

        prefix = out_name
        if os.path.exists(prefix + '.mp4'):
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
    def start_merge(cls, path, delete=False):
        if os.path.exists(path) and os.path.isdir(path):
            path = os.path.abspath(path)  # 将路径替换为绝对路径
            sub_dir_list = os.listdir(path)  # 获取路径下文件夹列表.
            for sub_dir in sub_dir_list:
                sub_path = os.path.join(path, sub_dir)
                if os.path.exists(sub_path) and os.path.isdir(sub_path):
                    file_list = os.listdir(sub_path)

                    flv_list = []
                    file_name = ""
                    for file in file_list:
                        file_path = os.path.join(sub_path, file)
                        # file_path = path + '\\' + file
                        file_name = os.path.splitext(file)[0]
                        prefix, suffix = os.path.splitext(file_path)
                        if suffix == '.flv':
                            flv_list.append(file_path)

                        elif suffix == '.mp4':
                            print_1('视频', end='')
                            print_cyan(file_name, end='')
                            print_1('已找到，跳过该文件')
                            break

                    cls.merge_fragment(flv_list, file_name, delete)

        else:
            raise BaseException('输入的文件夹路径不存在')
