#!/usr/bin/env python
#-*- coding:utf-8 -*-
import ConfigParser
from email.MIMEText import MIMEText
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
import os

import sys
import smtplib


def _send_email(to_addrs, subject, body):
    config_in_d = get_config_in_d()

    smtp = smtplib.SMTP()

    if config_in_d['debug']:
        smtp.set_debuglevel(1)

    code, msg = smtp.connect(host=config_in_d['smtp_host'], port=config_in_d['smtp_port'])
    assert code == 220

    code, msg = smtp.ehlo()
    assert code == 250

    code, msg = smtp.starttls()
    assert code == 220

    code, msg = smtp.login(user=config_in_d['username'], password=config_in_d['password'])
    assert code == 235

    msg = MIMEMultipart()
    text = MIMEText(body, "html", "utf-8")
    msg.attach(text)

    msg["From"] = config_in_d['username']
    msg["To"] = ";".join(to_addrs)
    msg["Subject"] = Header(subject, "utf-8")
    smtp.sendmail(from_addr=config_in_d['username'], to_addrs=to_addrs, msg=msg.as_string())
    smtp.quit()

def send_email(to_addrs, subject, body):
    try:
        _send_email(to_addrs, subject, body)
        return 0
    except Exception:
        import traceback
        traceback.print_exc(3, sys.stderr)
        return -1

def get_config_in_d():
    config_full_path = os.path.expanduser("~/.config/send_email.conf")
    config = ConfigParser.ConfigParser()
    config.read(config_full_path)
    return dict(
        smtp_host = config.get('main', 'smtp_host'),
        smtp_port = config.get('main', 'smtp_port'),
        username = config.get('main', 'username'),
        password = config.get('main', 'password'),
        debug = config.getint('main', 'debug'),
    )


def show_help():
    print "Usage: %s <to_contact> <subject> <body>" % sys.argv[0]

def test_send_email():
    subject = u"又挂了"
    body = u"又挂了"
    send_email(to_addrs=['bot@example.com'],
        subject=subject,
        body=body)

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or len(args) != 3:
        show_help()
        exit(1)
    else:
        to_contact, subject, body = args[0].strip(), args[1], args[2]
        exit(send_email([to_contact], subject, body))
        
    
