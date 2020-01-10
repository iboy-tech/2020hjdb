# -*- coding:utf-8 -*-

from flask import Flask
from flask import request
import  requests
import  ast


import hashlib

APPID='wx18d48283a9869675'
APPSECRET='7d8ff3809716bba9b05aa489bb931ef6'

app = Flask(__name__)
app.debug = True
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True




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

@app.route('/wx_flask',methods=['GET','POST'])
def wechat():
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


if __name__ == '__main__':
    app.run()