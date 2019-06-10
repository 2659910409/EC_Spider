import time
import datetime


# 睡眠时间，单位秒
def sleep(s):
    time.sleep(s)


def get_current_date():
    current_date = datetime.datetime.now().date()
    return current_date


def get_current_timestamp():
    current_timestamp = datetime.datetime.now()
    return current_timestamp


def date_add(date, day_num):
    """
    :param date: 需要做加减的日期
    :param day_num: 加减的天数,为正值代表加上相应的天数,为负值则代表减去相应天数
    :return: 结果日期,为YYYY-MM-DD格式
    """
    result_date = date + datetime.timedelta(days=day_num)
    return result_date


def get_last_month_date(date):
    """
    :param date: 指定日期
    :return: 指定日期的前一个月的开始日期与结束日期
    """
    start_date = date.replace(day=1).replace(month=date.month-1)
    end_date = date_add(date.replace(day=1), -1)
    return start_date, end_date


def date_to_string(date_time):
    """
    :param date_time: 日期或时间戳类型
    :return: 日期格式为YYYY-MM-DD的字符串
    """
    date_str = date_time.strftime('%Y-%m-%d')
    return date_str


def string_to_date(string, fmt):
    """
    :param string: 字符串型的日期或时间戳
    :param fmt: 需要转化的日期格式
    :return:格式为YYYY-MM-DD的日期
    """
    date = datetime.datetime.strptime(string, fmt).date()
    return date


def get_day_report_rule1():
    """

    :return:
    """
    # if 15号或之前
    # start_date = 上月1号
    # else 15号之前
    # start_date = 本月1号
    start_date = None
    # 当天
    end_date = None
    return start_date, end_date


