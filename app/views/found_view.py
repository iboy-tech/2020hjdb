# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : found_view.py
@Time    : 2020/1/24 20:35
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import base64

from flask import render_template, request, current_app
from flask_login import current_user
from sqlalchemy import desc, or_

from app import db
from app.main import found
from app.models.category_model import Category
from app.models.comment_model import Comment
from app.models.lostfound_model import LostFound
from app.models.user_model import User


@found.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    return render_template('found.html')


@found.route('/getall', methods=['POST'], strict_slashes=False)
def get_all():
    req = request.json
    page = int(req['pageNum'])
    print(req)
    print('get_users收到请求')
    keyword=req['keyword']
    pagination=None
    if req['kind'] == -1 and req['category'] == '' and req['username'] == '' and keyword=='':
        pagination = LostFound.query.order_by(desc('create_time')).paginate(page + 1, per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)

    elif req['kind'] == -1 and req['category'] != '':
        c = Category.query.filter_by(name=req['category']).first()
        pagination = LostFound.query.filter_by(category_id=c.id).order_by(desc('create_time')).paginate(page + 1,per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
    elif req['username'] != '':
        print('这是用户个人查询')
        u = User.query.filter_by(username=req['username']).first()
        pagination = LostFound.query.filter_by(user_id=u.id).order_by(desc('create_time')).paginate(page + 1, per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
    elif req['kind'] != -1 and req['category'] != '':
        print('这是分类查询')
        print(req['category'])
        c = Category.query.filter_by(name=req['category']).first()
        print('Category.query.',c)
        pagination = LostFound.query.filter_by(category_id=c.id,kind=req['kind']).order_by(desc('create_time')).paginate(page + 1,per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
    elif req['kind'] != -1 and req['category'] == '':
        print('这是分类查询')
        c = Category.query.filter_by(name=req['category']).first()
        pagination = LostFound.query.filter_by(kind=req['kind']).order_by(desc('create_time')).paginate(page + 1,per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
    elif keyword!='':
        print('这是分类查询')
        c = Category.query.filter(Category.name.like(("%" + keyword + "%"))).first()
        u=User.query.filter(or_(User.real_name.like("%" + keyword + "%"),
                                User.username.like("%" + keyword + "%")
                                )).first()
        if c is not None and u is not None:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.category_id==c.id,
                    LostFound.user_id==u.id)
            ).order_by(desc('create_time')).paginate(page + 1,per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
        elif c is not None and u is  None:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.category_id==c.id)
            ).order_by(desc('create_time')).paginate(page + 1,per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
        elif c is  None and u is not None:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.user_id==u.id)
            ).order_by(desc('create_time')).paginate(page + 1,per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
        elif ('寻物' or '寻' or '启' or '事' )in keyword:
            pagination = LostFound.query.filter(
                LostFound.kind==0
            ).order_by(desc('create_time')).paginate(page + 1, per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],
             error_out=False)
        elif ('认领'or'失' or '招' or '领' or '认') in keyword:
            pagination = LostFound.query.filter(
                LostFound.kind==1
            ).order_by(desc('create_time')).paginate(page + 1, per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],
             error_out=False)
        else:
            pagination = LostFound.query.filter(
                or_(LostFound.title.like("%" + keyword + "%"),
                    LostFound.about.like("%" + keyword + "%"),
                    LostFound.location.like("%" + keyword + "%"))
            ).order_by(desc('create_time')).paginate(page + 1, per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'],error_out=False)
    else:
        pagination = LostFound.query.filter(
            or_(LostFound.title.like("%" + keyword + "%"),
                LostFound.about.like("%" + keyword + "%"),
        )).order_by(desc('create_time')).paginate(page + 1, per_page=current_app.config['ARTISAN_POSTS_PER_PAGE'], error_out=False)
    data=get_search_data(pagination,page)
    print('分类查询：',data)
    return data


@found.route('/pub', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def pub():
    data = request.json
    print(data)
    print(data['images'], type(data['images']))
    imgstr = str(data['images'])
    print(type(imgstr), imgstr)
    lost = LostFound(kind=data['applyKind'], category_id=data['categoryId'],
                     images=imgstr, location=data['location'],
                     title=data['title'], about=data['about'], user_id=current_user.id)
    db.session.add(lost)
    db.session.commit()
    # print(data['images'][0],len(data['images']))
    # strs=data['images'][0]
    # with open('test.jpeg', 'wb') as f:
    #     f.write(base64.b64decode(strs))
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {},
        "ext": None
    }
    return data

def get_search_data(pagination,pageNum):
    losts = pagination.items
    print(losts)
    datalist = []
    for l in losts:
        print(l.images, type(l.images))
        l.images = l.images.replace('[', '').replace(']', '').replace(' \'', '').replace('\'', '')
        # print(l.images, type(l.images))
        imglist = l.images.strip().split(',')
        # print(imglist, type(imglist))
        user = User.query.get(l.user_id)
        dict = {
            "id": l.id,
            "icon": 'https://q2.qlogo.cn/headimg_dl?dst_uin={}&spec=100'.format(user.qq),
            "kind": l.kind,
            "status": l.status,
            "claimantId": l.claimant_id,
            "userId": l.user_id,
            "username": user.username,
            "realName": user.real_name,
            "time": l.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "location": l.location,
            "title": l.title,
            "about": l.about,
            "images": imglist,
            "category": Category.query.get(l.category_id).name,
            "lookCount": l.look_count,
            "commentCount": len(Comment.query.filter_by(lost_found_id=l.id).all())
        }
        datalist.append(dict)
    data = {
        "success": True,
        "code": 1000,
        "msg": "处理成功",
        "data": {
            "page": {
                "total": pagination.total,
                "totalPage": pagination.pages,
                "pageNum": pageNum,
                "pageSize": current_app.config['ARTISAN_POSTS_PER_PAGE'],
                "list": datalist
            }
        },
        "ext": None
    }
    return data

