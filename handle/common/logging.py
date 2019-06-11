

class Logging:
    def info(*s):
        """
        正常输出日志
        :param s:
        :return:
        """
        print(s)

    def debug(*s):
        """
        调试时输出详细日志
        :param s:
        :return:
        """
        print(s)

    def warning(*s):
        """
        不符合逻辑但并非异常，不影响程序执行的情况，告警
        :param s:
        :return:
        """
        print(s)

    def error(*s):
        """
        异常，当前过程执行失败
        :param s:
        :return:
        """
        print(s)


if __name__ == '__main__':
    Logging.info(1, 2, 3, '你好')
