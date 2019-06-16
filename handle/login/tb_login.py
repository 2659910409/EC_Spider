# -*- coding:utf-8 -*-
# ! python3

from time import sleep
from subprocess import Popen
from pywinauto.findwindows import find_windows
from retry import retry
from timeout3 import timeout
import ctypes
import socket
import pyautogui
from random import randint, uniform
from datetime import datetime
import logging
LOGIN_URL = ''


class TaoLogin:
    def __init__(self, shop_id, shopname, user_data_dir , profile_dir, port=9000):
        self.shop_id = shop_id
        self.shopname = shopname
        self.user_data_dir = user_data_dir
        self.profile_dir = profile_dir
        self.port = port
        while not self.check_port(self.port):
            self.port += 1
        logging.info('init 初始化完成获取到的店铺为：{}，端口为{}'.format(self.shopname, self.port))

    def check_port(port, ip='127.0.0.1'):
        '''
        :param port: 端口地址
        :param ip: 检测ip
        :return: 占用返回0，不占用返回其他值
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s.connect_ex((ip, port))

    def get_all_chrome_handle(self):
        '''
        :return: 所有打开的chrome浏览器句柄
        '''
        return find_windows(class_name='Chrome_WidgetWin_1')

    @retry(tries=3, delay=2)
    def start_chrome(self):
        # self.close_before_chrome()
        logging.info('已作关闭之前chrome处理，准备开始启动指定浏览器，店铺：{}'.format(self.shopname))
        # access = 'chrome --start-maximized {} --profile-directory="{}" --user-data-dir="{}" --remote-debugging-port={}'.format(LOGIN_URL, PROFILE_DIR, USER_DATA_DIR, self.port)
        access = 'chrome --start-maximized {} --remote-debugging-port={}'.format(LOGIN_URL, self.port)
        logging.info('店铺：{}，启动参数：{}'.format(self.shopname, access))
        before_handle = self.get_all_chrome_handle()
        p = Popen(access)
        try:
            self.handle = self.check_chrome_start(before_handle)
            logging.info('店铺:{},获取到新的chrome窗口句柄为：{}'.format(self.shopname, self.handle))
            ctypes.windll.user32.ShowWindow(self.handle, 3)  # 最大化窗口
            sleep(0.5)
            ctypes.windll.user32.SetForegroundWindow(self.handle)  # 将窗口放到前台top
            sleep(2)
            # self.update_chrome_info(self.handle, p.pid)
            self.check_page_error()
        except Exception as e:
            logging.error('店铺：{}，启动chrome失败，错误信息：{}'.format(self.shopname, e))
            p.kill()

    @timeout(seconds=30)
    def check_chrome_start(self, before_handle):
        while True:
            after_handle = self.get_all_chrome_handle()
            chrome_handle = list(set(after_handle) - set(before_handle))
            if chrome_handle:
                return chrome_handle[0]
            sleep(1)

    @timeout(seconds=30)
    def wait_load_ok(self):
        while True:
            rect = pyautogui.locateOnScreen('./images/login_btn.png', region=(1242,321,465,404), confidence=0.8)
            if not rect:
                sleep(1)
            else:
                sleep(1)
                return

    def click_login_orgin(self):
        # 1175,275
        rect = pyautogui.locateOnScreen('./images/login_orgin.png', region=(1242,321,465,404), confidence=0.8)
        pyautogui.click(rect[0] + 25, rect[1] + 38)
        sleep(1)
        pyautogui.click(rect[0], rect[1])
        sleep(1)

    def check_span(self):
        return pyautogui.locateOnScreen('./images/span.png', region=(1242,321,465,404), confidence=0.8)

    def check_move_span_ok(self):
        return pyautogui.locateOnScreen('./images/span_ok.png', region=(1242,321,465,404), confidence=0.8)

    def click_span_refresh(self):
        rect = pyautogui.locateOnScreen('./images/span_refresh.png', region=(1242,321,465,404), confidence=0.8)
        if not rect:
            raise Exception
        x = int((rect[0] * 2 + rect[2]) / 2)
        y = int((rect[1] * 2 + rect[3]) / 2)
        pyautogui.click(x, y)
        sleep(1)

    @retry(tries=5, delay=1)
    def move_span(self):
        if not self.check_login_ok():
            return
        pyautogui.hscroll(-100)
        sleep(0.3)
        # print('hsroll')
        sleep(1)
        rect = pyautogui.locateOnScreen('./images/span.png', region=(1242,321,465,404), confidence=0.8)
        x = int((rect[0] * 2 + rect[2]) / 2)
        y = int((rect[1] * 2 + rect[3]) / 2)
        pyautogui.moveTo(x, y, 0.5, pyautogui.easeInOutCirc)
        pyautogui.mouseDown(button='left', duration=uniform(0.05, 0.1))
        pyautogui.moveTo(x + 240, y + randint(-10, 10), uniform(0.5, 1.3), pyautogui.easeOutQuad)
        pyautogui.mouseUp(button='left', duration=uniform(0.05, 0.1))
        sleep(1)
        logging.info('拉动滑块结束，店铺：{}'.format(self.shopname))
        #  检测是否成功
        if not self.check_move_span_ok():
            logging.warning('拉动滑块失败，店铺：{}'.format(self.shopname))
            pyautogui.click(x, y)
            sleep(0.3)
            self.click_span_refresh()
            raise Exception
        sleep(1)
        logging.info('拉动滑块成功,店铺：{}'.format(self.shopname))

    @timeout(seconds=60 * 5)
    def warning_and_wait_people(self):
        title = '营销推广测试'
        text = '店铺:{},\n' \
               '时间:{},\n' \
               '登录需要短信验证，请及时处理'.format(self.shopname, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # TODO 钉钉告警
        # utils.sendDingDingMessage(DingDingGroupURL, title, text)
        while self.check_login_ok():
            sleep(1)

    def check_msg(self):
        rect = pyautogui.locateOnScreen('./images/msg_check.png', region=(1242,321,465,404), confidence=0.8)
        if rect:
            logging.warning('点击登录按钮并等待3S之后出现短信验证框，将发送告警信息并等待人工处理，店铺：{}'.format(self.shopname))
            self.warning_and_wait_people()
        else:
            logging.info('点击登录按钮并等待3S之后没有出现短信验证框,店铺：{}'.format(self.shopname))
            sleep(1)

    def test_RGB(self, x, y, rgb, to=0):
        return pyautogui.pixelMatchesColor(int(x), int(y), rgb, tolerance=to)

    def check_login_ok(self):
        focus_handle = ctypes.windll.user32.GetForegroundWindow()
        if not focus_handle == self.handle:
            ctypes.windll.user32.SetForegroundWindow(self.handle)
            sleep(1)
        return self.test_RGB(150, 110, (255, 255, 255), to=20)

    @timeout(seconds=30)
    def wait_login_ok(self):
        while self.check_login_ok():
            sleep(1)
        logging.info('点击登录按钮3S后，等待页面跳转完成，店铺：{}'.format(self.shopname))
        sleep(1)

    def get_login_btn_locate(self):
        login_locate = pyautogui.locateOnScreen('./images/login_btn.png', region=(1242,321,465,404), confidence=0.8)
        center_x = int((login_locate[0] * 2 + login_locate[2]) / 2)
        center_y = int((login_locate[1] * 2 + login_locate[3]) / 2)
        return center_x, center_y

    def check_login_btn(self):
        pyautogui.hscroll(-100)
        sleep(0.5)
        rect = pyautogui.locateOnScreen('./images/login_btn.png', region=(1242,321,465,404), confidence=0.8)
        if rect:
            logging.error('等待3S后登录按钮仍然在页面上,将结束本次登录，店铺：{}'.format(self.shopname))
            raise Exception

    def check_page_error(self):
        if self.test_RGB(1000, 25, (255, 255, 255), 10) and self.test_RGB(1200, 25, (255, 255, 255), 10):
            page_error_btn = pyautogui.locateOnScreen('./images/page_error.png', region=(1800, 0, 150, 150),
                                                      confidence=0.8)
            center_x = int((page_error_btn[0] * 2 + page_error_btn[2]) / 2)
            center_y = int((page_error_btn[1] * 2 + page_error_btn[3]) / 2)
            pyautogui.click(center_x, center_y)
            sleep(1)

    @retry(tries=3, delay=2)
    def parse_login(self):
        pyautogui.press('f5')
        if not self.check_login_ok():
            logging.info('检测到店铺已经进入到生意参谋主页，无需作登录操作，店铺：{}'.format(self.shopname))
            return
        logging.info('开始处理店铺，刷新,店铺：{}'.format(self.shopname))
        self.wait_load_ok()
        logging.info('页面加载完成，店铺：{}'.format(self.shopname))
        # print('page load ok')
        self.click_login_orgin()
        logging.info('点击login用户名和登录框,店铺：{}'.format(self.shopname))
        # print('click login orgin')
        sleep(1)
        if self.check_span():
            logging.warning('检测到滑块，店铺：{}'.format(self.shopname))
            self.move_span()
            logging.info('拉动滑块成功，店铺：{}'.format(self.shopname))
            x1, y1 = self.get_login_btn_locate()
            pyautogui.click(x1, y1)
        else:
            x2, y2 = self.get_login_btn_locate()
            logging.info('')
            pyautogui.click(x2, y2)
            sleep(1)
            if self.check_span():
                logging.warning('点击登录按钮后，检测到滑块，店铺：{}'.format(self.shopname))
                self.move_span()
                logging.info('点击登录按钮后，拉动滑块成功，店铺：{}'.format(self.shopname))
                x3, y3 = self.get_login_btn_locate()
                pyautogui.click(x3, y3)
        # print('click ok')
        logging.info('登录页处理前半部分完成，开始等待页面跳转店铺：{}'.format(self.shopname))
        sleep(3)
        if self.check_login_ok():
            logging.info('检测到等待3S后仍然未跳转到生意参谋主页面，将开始检测登录按钮，短信验证或页面加载缓慢逻辑，店铺：{}'.format(self.shopname))
            self.check_login_btn()
            logging.info('检测到等待3S后未检测到登录按钮，店铺：{}'.format(self.shopname))
            self.check_msg()
            # print('start wait')
            self.wait_login_ok()
            # print('login ok')

    def run(self):
        logging.info('登录程序，开始初始化chrome，店铺：{}'.format(self.shopname))
        self.start_chrome()
        logging.info('登录初始化成功，开始处理登录过程，店铺：{}'.format(self.shopname))
        self.parse_login()
        logging.info('登录处理成功，店铺：{}'.format(self.shopname))
        sleep(1)
        try:
            ctypes.windll.user32.ShowWindow(self.handle, 6)
            sleep(1)
            logging.info('已将店铺作最小化处理，店铺：{}'.format(self.shopname))
        except Exception as e:
            logging.error('店铺最小化失败，店铺：{}，错误信息：{}'.format(self.shopname, e))
