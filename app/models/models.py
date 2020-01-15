# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : models.py
@Time    : 2020/1/10 16:58
@Author  : iBoy
@Email   : iboy@iboy.tech
@Software: PyCharm
"""
#数据库连接
import pymysql
# 连接数据库
def get_coon():
    conn = pymysql.connect(host='数据库地址',
                           user='数据库用户名',
                           password='数据库密码',
                           port=3306,
                           db='数据库名称',
                           charset='utf8')
    return conn
class User(object):
    #构造函数
    def __init__(self,usr,pwd):
        self.usr=usr
        self.pwd=pwd
    def save(self):
        conn=get_coon()
        cur=conn.cursor()
        sql='insert '
        conn.close()

    def __str__(self):
        return 'usr:{},pwd:{}'.format(self.usr,self.pwd)


