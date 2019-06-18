import time
import datetime
from dateutil.relativedelta import relativedelta


# 睡眠时间，单位秒
def sleep(s):
    time.sleep(s)


def get_current_date():
    current_date = datetime.datetime.now().date()
    return current_date


def get_current_timestamp():
    current_timestamp = datetime.datetime.now()
    return current_timestamp


def add_day(date, days):
    """
    :param date: 需要做加减的日期
    :param day_num: 加减的天数,为正值代表加上相应的天数,为负值则代表减去相应天数
    :return: 结果日期,为YYYY-MM-DD格式
    """
    result_date = date + datetime.timedelta(days=days)
    return result_date


def add_month(date, months):
    date = date + relativedelta(months=months)
    return date


def get_last_month_date(date):
    """
    :param date: 指定日期
    :return: 指定日期的前一个月的开始日期与结束日期
    """
    start_date = date.replace(day=1).replace(month=date.month-1)
    end_date = add_day(date.replace(day=1), -1)
    return start_date, end_date


def date_to_string(date_time, fmt):
    """
    :param date_time: 日期或时间戳类型
    :return: 日期格式为YYYY-MM-DD的字符串
    """
    date_str = date_time.strftime(fmt)
    return date_str


def string_to_date(string, fmt):
    """
    :param string: 字符串型的日期或时间戳
    :param fmt: 需要转化的日期格式
    :return:格式为YYYY-MM-DD的日期
    """
    date = datetime.datetime.strptime(string, fmt).date()
    return date

def get_day_report_rule1(date):
    """
    获取日报的开始日期和结束日期
    :return:当前日期的前15日为开始日期,当前日期的前1日为结束日期
    """
    start_date = add_day(get_current_date(), -1)
    end_date = add_day(get_current_date(), -15)
    return start_date, end_date

def get_day_report_rule2(date):
    """
    获取日报的开始日期和结束日期
    :return:当前日期前一个月份的开始日期与当前日期
    """
    if date.day <= 15:
        start_date = add_month(date, -1).replace(day=1)
    if date.day > 15:
        start_date = date.replace(day=1)
    end_date = date
    return start_date, end_date


def get_month_report_rule(date):
    """
    获取月报的开始日期与结束日期
    :return:当前日期前一个月份的开始日期与结束日期
    """
    start_date = add_month(date, -1).replace(day=1)
    end_date = add_day(date.replace(day=1), -1)
    return start_date, end_date


