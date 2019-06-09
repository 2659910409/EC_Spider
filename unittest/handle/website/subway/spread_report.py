from handle.login.tb_login import TaoLogin
from handle.website.subway.spread_report import SpreadReportDay
# from handle.website.subway.spread_report import SpreadReportMonth


if __name__ == '__main__':
    # 测试登录
    SHOP_NAME = '皇家美素佳儿旗舰店'
    SHOP_ID = 1
    DingDingGroupURL = 'https://oapi.dingtalk.com/robot/send?access_token=b65e1a4b8830dcde33c49c0b1ea559263d46eb6f0797dfff24cb2f662888a78a'
    LOGIN_URL = 'https://sycm.taobao.com/portal/home.htm'
    USER_DATA_DIR = "D:/chrome_user/Default"
    PROFILE_DIR = "Default"
    tb = TaoLogin(SHOP_ID, SHOP_NAME, USER_DATA_DIR, PROFILE_DIR)
    port = tb.port
    tb.run()
    # 测试数据抓取与入库
    store_name = None
    data_page = None

    spread_report_day = SpreadReportDay(store_name, data_page).run()

