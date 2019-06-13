#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-6-11
# @Author  : Luopan
# @Dec     : 读写配置文件
import configparser
import src.global_parameter


class Readconfig(object):
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.file_path = src.global_parameter.project_path + "\\config.ini"

    def get_config_values(self, section, option):
        self.cfg.read(self.file_path, encoding='UTF-8')
        return self.cfg.get(section=section, option=option)


if __name__ == '__main__':
    rf = Readconfig()
    result = rf.get_config_values("baseinfo", "DeviceId")
    print(result)