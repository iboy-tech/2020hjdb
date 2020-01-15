# -*- coding:utf-8 -*-
import ast
import hashlib
import json
import time

import requests
import xmltodict
from flask import request, Flask,render_template
from app.config import  *

app = Flask(__name__)
# app.debug = True
# app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.route('/get_access_token',methods=['GET'])
def access_token():
    resp=requests.get(' https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+APPID+'&secret='+APPSECRET)
    # print(resp,type(resp))
    # print(resp.text,type(resp.text))
    # obj=json.load(resp.text)
    data=ast.literal_eval(resp.text)
    # print(data,type(data))
    # print(obj,type(obj))
    # print(obj.get('access_token'))
    return  data.get('access_token')
ACCESS_TOKEN=access_token()

@app.route('/get_callback_ip',methods=['GET'])
def callback_ip():
    resp=requests.get(' https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+APPID+'&secret='+APPSECRET)
    return  resp.text

@app.route('/get_template_list',methods=['GET'])
def template_list():
    resp=requests.get('https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token='+ACCESS_TOKEN)
    return  resp.text

@app.route('/',methods=['GET'])
def index():
    return  render_template("index.html")

@app.route('/set_industry',methods=['POST'])
def set_industry():
    data={
    "industry_id1":"2",
    "industry_id2":"17"
    }
    print(ACCESS_TOKEN)
    resp=requests.post('https://api.weixin.qq.com/cgi-bin/template/api_set_industry?access_token='+ACCESS_TOKEN,data=data)
    return  resp.text
print(set_industry())

@app.route('/get_industry',methods=['GET'])
def get_industry():
    print(ACCESS_TOKEN)
    resp=requests.get('https://api.weixin.qq.com/cgi-bin/template/get_industry?access_token='+ACCESS_TOKEN)
    return  resp.text

@app.route('/send_message',methods=['POST'])
def send_message(OPENID,):
    print(ACCESS_TOKEN)
    data={
    "touser":OPENID,
    "msgtype":"text",
    "text":
    {
         "content":"Hello World"
    }
    }
    resp=requests.post('https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='+ACCESS_TOKEN,data=data )
    return  resp.text
send_message('oIBxm00mUNv4mkVAgjBpwvyJqbb0')

def resp_by_msg_type(xml_dict):
    # 提取消息类型
    msg_type = xml_dict.get("MsgType")
    if msg_type == "text":
        # 表示发送的是文本消息
        # 构造返回值，经由微信服务器回复给用户的消息内容
        resp_dict = {
            "xml": {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": "you say:" + xml_dict.get("Content")
            }
        }

        # 将字典转换为xml字符串
        resp_xml_str = xmltodict.unparse(resp_dict)
        # 返回消息数据给微信服务器
        return resp_xml_str
    # 收到图片消息
    if msg_type == "image":
        # 表示发送的是文本消息
        # 构造返回值，经由微信服务器回复给用户的消息内容
        resp_dict = {
            "xml": {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "PicUrl": xml_dict.get("PicUrl"),
                "MediaId": xml_dict.get("MediaId"),
                # "MsgId" : xml_dict.get("MsgId")
                "MsgId": "1234567890123456"
            }
        }

        # 将字典转换为xml字符串
        resp_xml_str = xmltodict.unparse(resp_dict)
        # 返回消息数据给微信服务器
        return resp_xml_str
    else:
        resp_dict = {
            "xml": {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": "欢迎关注CTGU小助手！"
            }
        }
        resp_xml_str = xmltodict.unparse(resp_dict)
        # 返回消息数据给微信服务器
        return resp_xml_str

@app.route('/wx_pusher',methods=['GET','POST'])
def wx_pusher():
    # 第一次接入服务器的验证
        #这里改写你在微信公众平台里输入的token
        #获取输入参数
        data = request.args
        print(data)
        # return  data


@app.route('/wx_flask',methods=['GET','POST'])
def wechat():
    # 第一次接入服务器的验证
    if request.method == 'GET':
        #这里改写你在微信公众平台里输入的token
        token = 'ctgu'
        #获取输入参数
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        #字典排序
        list = [token, timestamp, nonce]
        list.sort()

        s = list[0] + list[1] + list[2]
        #sha1加密算法        
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        #如果是来自微信的请求，则回复echostr
        if hascode == signature:
            return echostr
        else:
            return "非微信官方请求"
    #回复用户消息
    elif request.method == "POST":
        # 表示微信服务器转发消息过来
        xml_str = request.data
        if not xml_str:
            return "不支持此此类型消息处理！"
        # 对xml字符串进行解析
        xml_dict = xmltodict.parse(xml_str)
        xml_dict = xml_dict.get("xml")
        return resp_by_msg_type(xml_dict)

class Menu(object):
    def create(self, postData):
        p = json.dumps(postData, ensure_ascii=False)
        postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % AccessToken.get_access_token()
        req = requests.post(postUrl, p.encode('utf-8'))
        print(req.text)


def getMenu():
    postJson = {
        "button": [
            {
                "name": "公共查询",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "天气查询",
                        "key": "tianQi"
                    }]
            }]
    }

    return postJson


if __name__ == '__main__':
    # pData = getMenu()
    # m = Menu()
    # m.create(pData)
    app.run(debug=True)