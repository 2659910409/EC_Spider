
def sendDingDingMessage(posturl, title, text):
    """发送钉钉消息"""
    text = title + '\n' + text
    # 群：爬虫系统开发
    data = {"msgtype": "text", "text": {"content": text}, "at": {"atMobiles": [], "isAtAll": False}}
    data = json.dumps(data)
    data = bytes(data, 'utf-8')
    req = request.Request(posturl, headers={"Content-Type": "application/json; charset=utf-8"})
    response = request.urlopen(req, data)
    return response.read()
