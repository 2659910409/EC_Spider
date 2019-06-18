from enum import Enum


class ErrorMsg:
    """
    异常实例
    """
    def __init__(self, err_code, err_msg):
        self.err_code = err_code
        self.err_msg = err_msg
        if err_code[0] == '9':
            self.err_type = '系统级别异常'
        elif err_code[0] == '1':
            self.err_type = '取数-初始化任务'
        elif err_code[0] == '2':
            self.err_type = '取数-登录操作'
        elif err_code[0] == '3':
            self.err_type = '取数-页面操作'
        elif err_code[0] == '4':
            self.err_type = '取数-页面文件下载'
        elif err_code[0] == '5':
            self.err_type = '取数-数据处理'
        elif err_code[0] == '6':
            self.err_type = '取数-数据入库'
        elif err_code[0] == '7':
            self.err_type = '取数-数据备份'
        else:
            self.err_type = '未知异常'

    def get_err_type(self):
        return self.err_type

    def get_err_code(self):
        return self.err_code

    def get_err_msg(self):
        return self.err_msg

    def set_msg(self, msg):
        self.err_msg = msg

    def print(self):
        print('err_type:', self.err_type, 'err_code:', self.err_code, ',err_msg:', self.err_msg)


class ErrorEnum(Enum):
    """
    worker页面取数
    """
    # 系统级异常(9000-9999)
    ERROR_9999 = ErrorMsg('9999', '未知异常')
    ERROR_9001 = ErrorMsg('9001', '未匹配到任务实例')
    ERROR_9002 = ErrorMsg('9002', '未匹配到任务func')
    # 取数-初始化任务 1000-1999
    ERROR_1000 = ErrorMsg('1000', '未知异常')
    ERROR_1001 = ErrorMsg('1001', '店铺未登录')
    ERROR_1002 = ErrorMsg('1002', '店铺实例未找到')
    # 取数-登录操作 2000-2999
    ERROR_2000 = ErrorMsg('2000', '未知异常')
    # 取数-页面操作及文件下载/读取 3000-3999
    ERROR_3000 = ErrorMsg('3000', '未知异常')
    ERROR_3001 = ErrorMsg('3001', '页面请求失败')
    ERROR_3002 = ErrorMsg('3002', '控件操作失败')
    # 取数-数据处理 4000-4999
    ERROR_4000 = ErrorMsg('4000', '未知异常')
    # 取数-数据入库 5000-5999
    ERROR_5000 = ErrorMsg('5000', '未知异常')
    # 取数-数据备份 6000-6999
    ERROR_6000 = ErrorMsg('6000', '未知异常')
