# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : cache_view.py
@Time    : 2020/2/10 16:22
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 操作后台缓存
@Software: PyCharm
"""
from flask import flash, redirect, url_for

from app.page import cached
from app import cache


@cached.route('/update/bar')
def update_bar():
    cache.delete('view/%s' % url_for('bar'))
    flash('Cached data for bar have been deleted.')
    return redirect(url_for('index'))


@cached.route('/update/baz')
def update_baz():
    cache.delete('view/%s' % url_for('baz'))
    flash('Cached data for baz have been deleted.')
