# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : userlist_view.py
@Time    : 2020/1/23 22:41
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from random import randint

from flask import render_template, request
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db, redis_client
from app.config import PostConfig
from app.decorators import super_admin_required, admin_required, wechat_required
from app.models.user_model import User
from app.page import userlist
from app.utils import restful
from app.utils.auth_token import generate_password
from app.utils.mail_sender import send_email
from app.views import found_view


@userlist.route('/', methods=['POST', 'GET', 'OPTIONS'], strict_slashes=False)
@login_required
@wechat_required
@admin_required
def index():
    return render_template('userlist.html')


@userlist.route('/getall', methods=['POST', 'GET'], strict_slashes=False)
@login_required
@wechat_required
@admin_required
# @cache.cached(timeout=10 * 60,query_string=True,key_prefix='user-getall')  # 缓存10分钟 默认为300s
def get_all():
    req = request.json
    print(req)
    page = int(req['pageNum'])
    pagesize = int(req['pageSize'])
    # 自动调整每页的数量
    total_page = db.session.query(User).count()
    mid = total_page // 10
    if pagesize < mid:
        pagesize = mid
    keyword = req['keyword']
    if keyword == '':
        print('get_users收到请求')
        pagination = User.query.order_by(User.kind.desc(), User.status, User.last_login.desc(),
                                         User.last_login.desc()).paginate(page + 1, per_page=pagesize,
                                                                          error_out=False)
        data = search(pagination, page, pagesize)
        return data
    else:
        if keyword == '男':
            pagination = User.query.filter(
                User.gender == 0).order_by(User.kind.desc(), User.status, User.last_login.desc()).paginate(page + 1,
                                                                                                           per_page=pagesize,
                                                                                                           error_out=False)
            data = search(pagination, page, pagesize)
            return data
        elif keyword == '女':
            pagination = User.query.filter(
                User.gender == 1).order_by(User.kind.desc(), User.status, User.last_login.desc()).paginate(page + 1
                                                                                                           ,
                                                                                                           per_page=pagesize,
                                                                                                           error_out=False)
            data = search(pagination, page, pagesize)
            return data
        elif '正常' in keyword:
            pagination = User.query.filter(
                User.status == 1).order_by(User.kind.desc(), User.status, User.last_login.desc()).paginate(page + 1,
                                                                                                           per_page=pagesize,
                                                                                                           error_out=False)
            data = search(pagination, page, pagesize)
            return data
        elif '冻结' in keyword:
            pagination = User.query.filter(
                User.status == 0).order_by(User.kind.desc(), User.status, User.last_login.desc()).paginate(page + 1,
                                                                                                           per_page=pagesize,
                                                                                                           error_out=False)
            data = search(pagination, page, pagesize)
            return data
        elif '认证' in keyword:
            pagination = User.query.filter(
                User.status == 2).order_by(User.kind.desc(), User.status, User.last_login.desc()).paginate(page + 1,
                                                                                                           per_page=pagesize,
                                                                                                           error_out=False)
            data = search(pagination, page, pagesize)
            return data
        elif '管理' in keyword:
            pagination = User.query.filter(
                User.kind >= 2).order_by(User.kind.desc(), User.status, User.last_login.desc()).paginate(page + 1,
                                                                                                         per_page=pagesize,
                                                                                                         error_out=False)
            data = search(pagination, page, pagesize)
            return data
        else:
            pagination = User.query.filter(or_(
                User.real_name.like("%" + keyword + "%"),
                User.username.like("%" + keyword + "%"),
                User.qq.like("%" + keyword + "%"),
                User.class_name.like("%" + keyword + "%"),
                User.major.like("%" + keyword + "%"),
                User.academy.like("%" + keyword + "%"),
                User.kind.like("%" + keyword + "%"),
            )).order_by(User.kind.desc(), User.status, User.last_login.desc()).paginate(page + 1, per_page=pagesize,
                                                                                        error_out=False)
        data = search(pagination, page, pagesize)
        return data


@userlist.route('/freeze', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def user_freeze_or_unfreeze():
    req = request.args.get('userId')
    u = User.query.get_or_404(int(req))
    if u.status == 1:
        return restful.success(success=False, msg='该账户尚未认证，暂时无法冻结')
    elif current_user.kind <= u.kind:
        return restful.success(success=False, msg='权限不足')
    elif u.status == 2:  # 级别高的才能操作
        u.status = 0
        messages = {
            'realName': u.real_name,
            'handlerName': current_user.real_name,
            'handlerEmail': current_user.qq + '@qq.com',
        }
        send_email.apply_async(args=(u.qq, '账户冻结通知', 'userFreeze', messages), countdown=randint(1, 30))
    elif u.status == 0:
        u.status = 2
        messages = {
            'realName': u.real_name,
            'handlerName': current_user.real_name,
            'handlerEmail': current_user.qq + '@qq.com',
        }
        send_email.apply_async(args=(u.qq, '账户恢复通知', 'userunFreeze', messages), countdown=randint(1, 30))
    print('要给用户发送提醒邮件')
    db.session.commit()
    return restful.success()


@userlist.route('/resetPassword', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def reset_pssword():
    req = request.args.get('userId')
    print('request.args', req)
    u = User.query.get(int(req))
    password = generate_password()
    u.password = password
    print('发送邮件')
    messages = {
        'username': u.username,
        'password': password,
        'realName': u.real_name,
        'handlerName': current_user.real_name,
        'handlerEmail': current_user.qq + '@qq.com',
    }
    print("我是新的密码", password)
    send_email.apply_async(args=(u.qq, '密码重置提醒', 'resetPassword', messages), countdown=randint(1, 30))
    print('要给用户发送提醒邮件')
    db.session.add(u)
    db.session.commit()
    return restful.success()


@userlist.route('/deleteAll', methods=['POST'], strict_slashes=False)
@super_admin_required
def delete_users():
    req = request.json
    print(req)
    if req:
        users = User.query.filter(User.id.in_(req))
        for u in users:
            if u.kind != 3:
                posts = u.posts
                print(posts, type(posts))
                del_imgs = []
                for lost in posts:
                    # 删除redis中的浏览量数据
                    key = str(lost.id) + PostConfig.POST_REDIS_PREFIX
                    redis_client.delete(key)
                    print(lost.images)
                    if lost.images == "":
                        temp_imglist = []
                    else:
                        lost.images = lost.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                        temp_imglist = lost.images.strip().split(',')
                    del_imgs += temp_imglist
                print("删除用户的所有图片")
                found_view.remove_imglist(del_imgs)
                try:
                    db.session.delete(u)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return restful.params_error(success=False, msg=str(e))
            # 无法直接删除超级管理员
            else:
                return restful.params_error(False, msg="超级管理员无法直接删除")
        return restful.success(msg="删除成功")
    else:
        return restful.params_error(False, msg="参数错误")
    return restful.success(msg="删除失败")


@userlist.route('/delete', methods=['POST'], strict_slashes=False)
@super_admin_required
def delete_user():
    req = request.args.get('userId')
    print('request.args', req)
    u = User.query.get(int(req))
    if u and u.kind != 3:
        try:
            posts = u.posts
            print(posts, type(posts))
            del_imgs = []
            for lost in posts:
                # 删除redis中的浏览量数据
                key = str(lost.id) + PostConfig.POST_REDIS_PREFIX
                redis_client.delete(key)
                print(lost.images)
                if lost.images == "":
                    temp_imglist = []
                else:
                    lost.images = lost.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
                    temp_imglist = lost.images.strip().split(',')
                del_imgs += temp_imglist
            print("删除用户的所有图片")
            found_view.remove_imglist.delay(del_imgs)
            db.session.delete(u)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return restful.params_error(success=False, msg=str(e))
    else:
        if u.kind == 3:
            return restful.params_error(False, msg="超级管理员无法直接删除")
        return restful.params_error(success=False, msg="用户不存在")
    return restful.success(msg="删除失败")


@userlist.route('/setAsAdmin', methods=['POST'], strict_slashes=False)
@super_admin_required
def set_or_cancle_admin():
    req = request.args.get('userId')
    print('request.args', req)
    u = User.query.get(int(req))
    u.kind = 2 if u.kind == 1 else 1
    db.session.commit()
    print('发送邮件')
    return restful.success()


# @cache.memoize(timeout=50)  # 根据参数设置缓存
def search(pagination, page, pagesize):
    global data
    users = pagination.items
    # users = User.query.order_by(desc('kind')).all()
    # print(users)
    list = []
    for u in users:
        dict = u.to_dict()
        list.append(dict)
        data = {
            "page": {
                "total": pagination.total,
                "totalPage": pagination.pages,
                "pageNum": page,
                "pageSize": pagesize,
                "list": list
            }
        }
    return restful.success(data=data)


@userlist.route('/userInfo', methods=['POST'], strict_slashes=False)
@login_required
@admin_required
def get_userinfo():
    id = int(request.args.get('userId'))
    u = User.query.get_or_404(id)
    data = {
        "user": u.to_dict()
    }
    return restful.success(data=data)
