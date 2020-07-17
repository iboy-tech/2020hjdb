# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : users_view.py
@Time    : 2020/1/23 22:41
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from random import randint

from flask import render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db, redis_client, cache, limiter, logger, OpenID
from app.config import PostConfig
from app.decorators import super_admin_required, admin_required, wechat_required
from app.models.user_model import User
from app.page import users
from app.utils import restful
from app.utils.auth_token import generate_password, generate_token
from app.utils.delete_file import remove_files
from app.utils.mail_sender import send_email


@users.route('/', methods=['POST'], strict_slashes=False)
@limiter.limit("2/day", exempt_when=lambda: current_user.is_admin)
@login_required
@wechat_required
@admin_required
# @cache.cached(timeout=10 * 60,query_string=True,key_prefix='user-getall')  # 缓存10分钟 默认为300s
def get_all():
    req = request.json
    page = int(req['pageNum'])
    pagesize = int(req['pageSize'])
    # 自动调整每页的数量
    total_page = db.session.query(User).count()
    mid = total_page // 10
    if pagesize < mid:
        pagesize = mid
    keyword = req['keyword']
    if keyword == '':
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


@users.route('/freeze/<int:id>', methods=['GET'], strict_slashes=False)
@login_required
@admin_required
def user_freeze_or_unfreeze(id=-1):
    if id == -1:
        return restful.error()
    u = User.query.get_or_404(id)
    if u.status == 1:
        return restful.error('该账户尚未认证，暂时无法冻结')
    elif current_user.kind <= u.kind:
        return restful.error('权限不足')
    elif u.status == 2:  # 级别高的才能操作
        u.status = 0
        messages = {
            'realName': u.real_name,
            'handlerName': current_user.real_name,
            'handlerEmail': current_user.qq + '@qq.com',
        }
        send_email.apply_async(args=(u.qq, '账户冻结通知', 'userFreeze', messages), countdown=randint(10, 30))
    elif u.status == 0:
        u.status = 2
        messages = {
            'realName': u.real_name,
            'handlerName': current_user.real_name,
            'handlerEmail': current_user.qq + '@qq.com',
        }
        send_email.apply_async(args=(u.qq, '账户恢复通知', 'userunFreeze', messages), countdown=randint(10, 30))
    db.session.commit()
    return restful.success()


@users.route('/password/<int:id>', methods=['GET'], strict_slashes=False)
@login_required
@admin_required
def reset_pssword(id=-1):
    if id == -1:
        return restful.error()
    u = User.query.get(id)
    password = generate_password()
    u.password = password
    messages = {
        'password': password,
        'realName': u.real_name,
    }
    send_email.apply_async(args=(u.qq, '密码重置提醒', 'resetPassword', messages), countdown=1)
    db.session.add(u)
    db.session.commit()
    return restful.success()


# 重新手动给用户发送认证邮件
@users.route('/resend/<int:id>', methods=['GET'], strict_slashes=False)
@login_required
@admin_required
def resend_mail(id=-1):
    if id == -1:
        return restful.error()
    try:
        user_db = User.query.get(id)
        token = str(generate_token(id=user_db.id, operation='confirm-qq', qq=user_db.qq), encoding="utf-8")
        messages = {
            'real_name': user_db.real_name,
            'token': url_for('auth.confirm', token=token, _external=True)
        }
        send_email.apply_async(args=(user_db.qq, '身份认证', 'confirm', messages), countdown=1)
        return restful.success(msg='发送成功')
    except:
        return restful.success(False, msg="参数错误")


def delete_img_and_report(posts, reports):
    del_imgs = []
    del_reports = []
    if posts:
        for lost in posts:
            key = PostConfig.POST_REDIS_PREFIX + str(lost.id)
            redis_client.delete(key)
            # logger.info(lost.images)
            if lost.images != "":
                temp_imglist = lost.images.split(',')
                del_imgs += temp_imglist
        # logger.info(del_imgs, type(del_imgs))
        remove_files(del_imgs, 0)
    if reports:
        for report in reports:
            del_reports.append(report.id + ".xlsx")
        remove_files(del_reports, 2)


@users.route('/', methods=['DELETE'], strict_slashes=False)
@super_admin_required
def delete_users():
    req = request.json
    if req:
        my_users = User.query.filter(User.id.in_(req)).all()
        flag = False
        try:
            for u in my_users:
                if u.kind != 3:
                    u = db.session.merge(u)
                    posts = u.posts
                    reports = u.reports
                    # 删除图片和报告
                    delete_img_and_report(posts, reports)

                    db.session.delete(u)
                    db.session.commit()
                    # db.session.close()
                    # users.remove(u)
                else:
                    flag = True
        except Exception as e:
            db.session.rollback()
            return restful.error(str(e))
        finally:
            db.session.close()
            # 无法直接删除超级管理员
        if flag:
            return restful.success(msg="已删除除超级管理员之外的用户")
        return restful.success(msg="删除成功")
    else:
        return restful.error("参数错误")
    return restful.success(msg="删除失败")


@users.route('/delete/<int:id>', methods=['DELETE'], strict_slashes=False)
@super_admin_required
def delete_user(id=-1):
    if id == -1:
        return restful.error()
    u = User.query.get(id)
    if u and u.kind != 3:
        try:
            posts = u.posts
            reports = u.reports
            delete_img_and_report(posts, reports)
            db.session.delete(u)
            db.session.commit()

        except Exception as e:
            logger.info(str(e))
            db.session.rollback()
            return restful.error()
    else:
        if u.kind == 3:
            return restful.error("超级管理员无法直接删除")
        return restful.error("用户不存在")
    return restful.success(msg="删除成功")


@users.route('/wechat/<int:id>', methods=['DELETE'], strict_slashes=False)
@super_admin_required
def delete_wechat(id=-1):
    if id == -1:
        return restful.error()
    op = OpenID.query.filter_by(user_id=id).first()
    if op is None:
        return restful.error("此用户尚未绑定微信")
    if current_user.kind <= op.user.kind:
        return restful.error("权限不足")
    try:
        db.session.delete(op)
        db.session.commit()
    except Exception as e:
        logger.info(str(e))
        db.session.rollback()
        return restful.error()
    messages = {
        'realName': op.user.real_name,
    }
    send_email.apply_async(args=(op.user.qq, '微信解绑提醒', 'resetWeChat', messages), countdown=2)
    return restful.success(msg="解绑成功")


@users.route('/admin/<int:id>', methods=['GET'], strict_slashes=False)
@super_admin_required
def set_or_cancle_admin(id=-1):
    if id == -1:
        return restful.error()
    u = User.query.get(id)
    u.kind = 2 if u.kind == 1 else 1
    db.session.commit()
    return restful.success()


# @cache.memoize(timeout=50)  # 根据参数设置缓存
def search(pagination, page, pagesize):
    global data
    my_users = pagination.items
    list = []
    for u in my_users:
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


@users.route('/info/<int:id>', methods=['GET'], strict_slashes=False)
@login_required
@admin_required
def get_userinfo(id=-1):
    if id == -1:
        return restful.error()
    u = User.query.get(id)
    if u:
        data = {
            "user": u.to_dict()
        }
        return restful.success(data=data)
    else:
        return restful.error("认领（或拾取）者已被删除")


