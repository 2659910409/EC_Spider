# -*- coding: utf-8 -*-
import time


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class Logging:

    @staticmethod
    def info(*ss):
        """
        正常输出日志
        :param s:
        :return:
        """
        _ss = []
        for s in ss:
            _ss.append(str(s))
        print(get_time(), '-INFO', ' '.join(_ss))

    @staticmethod
    def debug(*ss):
        """
        调试时输出详细日志
        :param s:
        :return:
        """
        _ss = []
        for s in ss:
            _ss.append(str(s))
        print(get_time(), '-DEBUG', ' '.join(_ss))

    @staticmethod
    def warning(*ss):
        """
        不符合逻辑但并非异常，不影响程序执行的情况，告警
        :param s:
        :return:
        """
        _ss = []
        for s in ss:
            _ss.append(str(s))
        print(get_time(), '-WARNING', ' '.join(_ss))

    @staticmethod
    def error(*ss):
        """
        异常，当前过程执行失败
        :param s:
        :return:
        """
        _ss = []
        for s in ss:
            _ss.append(str(s))
        print(get_time(), '-ERROR', ' '.join(_ss))


if __name__ == '__main__':
    Logging.info(1, 2, 3, '你好')
    Logging.error(1, 2, 3, '你好')
