#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: wxpusher.py
Author: huxuan
Email: i(at)huxuan.org
Description: WxPusher Python Client.
"""
import os

import requests

from . import exceptions

BASEURL = 'http://wxpusher.zjiecode.com/api'


class WxPusher():
    """WxPusher Python Client."""
    default_token = os.getenv('WX_PUSHER_TOKEN')

    @classmethod
    def send_message(cls, content, uids, token=None, **kwargs):
        print('这是环境变量中的token', cls.default_token)
        print('这是要发送的内容和对象', content, uids)
        """Send Message."""
        payload = {
            'appToken': cls.get_token(token),
            'content': content,
            'contentType': kwargs.get('content_type', 1),
            'topicIds': kwargs.get('topic_ids', []),
            'uids': uids,
            'url': kwargs.get('url')
        }
        url = BASEURL+'/send/message'
        return requests.post(url, json=payload).json()

    @classmethod
    def query_message(cls, message_id):
        """Query message status."""
        url = BASEURL+'/send/query/{message_id}'
        return requests.get(url).json()

    @classmethod
    def create_qrcode(cls, extra, valid_time=300, token=None):  # 二维码有效期默认30min
        """Create qrcode with extra callback information."""
        payload = {
            'appToken': cls.get_token(token),
            'extra': extra,
            'validTime': valid_time
        }
        url = BASEURL+'/fun/create/qrcode'
        return requests.post(url, json=payload).json()

    @classmethod
    def query_user(cls, page, page_size, token=None):
        """Query users."""
        payload = {
            'appToken': cls.get_token(token),
            'page': page,
            'pageSize': page_size
        }
        url = BASEURL+'/fun/wxuser'
        return requests.get(url, params=payload).json()

    @classmethod
    def get_token(cls, token=None):
        """Get token with validation."""
        token = token or cls.default_token
        if not token:
            raise exceptions.WxPusherNoneTokenException()
        return token
