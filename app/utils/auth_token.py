# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : auth_token.py
@Time    : 2020/2/7 13:07
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description :
@Software: PyCharm
"""
import string
from random import choice

from app.config import Operations
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer  as Serializer, SignatureExpired, BadSignature

# 生成邮箱验证TOKEN
from app import db, User
from app.utils import restful


def generate_password(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


def generate_token(id, operation, expire_in=172800, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(token):  # 验证邮箱
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        print(data)
        user = User.query.get(data['id'])
        print('要验证的用户', user.to_dict())
        if user is None:
            return restful.params_error(msg='验证信息有误')
    except (SignatureExpired, BadSignature):
        return restful.params_error(msg='验证信息错误或已过期')
    # if data.get('operation') != 'confirm' or user.qq != data.get('qq'):
    #     return restful.params_error(msg='验证途径非法')
    if data.get('operation') == Operations.CONFIRM_QQ:
        if user.status == 1:
            user.status = 2
            # 所有QQ只从token中获取
            user.qq = data.get('qq')
            db.session.commit()
            return restful.success(msg='恭喜,验证成功')
        else:
            return restful.params_error(msg='您已注册，请直接登录')
    if data.get('operation') == Operations.CHANGE_QQ:
        user.qq = data.get('qq')
        try:
            db.session.commit()
            return restful.success(msg='恭喜,QQ更改成功')
        except:
            db.session.rollback()
            return restful.success(msg='要更改的QQ已被使用')
    else:
        return restful.params_error(msg='更改失败,请重新尝试')

    return restful.params_error(msg='验证信息有误')
