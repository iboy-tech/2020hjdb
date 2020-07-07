# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : robot_view.py
@Time    : 2020/4/15 11:01
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
from flask import render_template, request
from flask_login import login_required

from app import db, logger
from app.decorators import admin_required, super_admin_required
from app.page import robot
from app.utils import restful
from app.models.robot_model import Robot


@robot.route("/", methods=["GET"])
@login_required
@admin_required
def index():
    return render_template('robot.html')


@robot.route("/getall", methods=['GET', 'POST', 'OPTIONS'])
@login_required
@admin_required
def get_all():
    robots = Robot.query.all()
    my_list = []
    if robots:
        my_list = [r.to_dict for r in robots]
    data = {
        "list": robots
    }
    return restful.success(data=data)


@robot.route("/add", methods=['GET', 'POST', 'OPTIONS'])
@login_required
@admin_required
def add_group():
    req = request.json
    id = req.get("id")
    if id == "":
        try:
            new_robot = Robot(key=req["key"], group_num=req["num"], group_name=req["name"])
            db.session.add(new_robot)
            db.session.commit()
        except Exception as e:
            return restful.error(str(e))
    else:
        update_robot = Robot.query.get(int(id))
        update_robot.key = req["key"]
        update_robot.group_num = req["num"]
        update_robot.group_name = req["name"]
        db.session.add(update_robot)
        db.session.commit()
        return restful.success(msg="修改成功")
    return restful.success(msg="添加成功")


@robot.route('/<int:id>', methods=['DELETE'])
@login_required
@super_admin_required
def delete(id):
    try:
        dg = Robot.query.get(int(id))
        db.session.delete(dg)
        db.session.commit()
        return restful.success(msg="删除成功")
    except Exception as e:
        return restful.error(str(e))
