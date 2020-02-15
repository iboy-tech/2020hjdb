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
from app.config import Operations
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer  as Serializer, SignatureExpired, BadSignature

# 生成邮箱验证TOKEN
from app import db, User
from app.utils import restful


def generate_token(user, operation, expire_in=172800, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
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
        return restful.params_error(msg='验证信息错误或已过期，请重新验证')
    # if data.get('operation') != 'confirm' or user.qq != data.get('qq'):
    #     return restful.params_error(msg='验证途径非法')
    if data.get('operation') == Operations.CONFIRM_QQ:
        if user.status == 1:
            user.status = 2
            db.session.commit()
            return restful.success(msg='恭喜,验证成功,即将返回登录页')
        else:
            return restful.params_error(msg='您已验证，请直接登录')
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
