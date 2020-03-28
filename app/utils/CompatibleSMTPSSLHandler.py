# -*- coding:UTF-8 -*-
#!/usr/bin/python
"""
@File    : CompatibleSMTPSSLHandler.py
@Time    : 2020/2/28 21:20
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import time
from logging import handlers


class CompatibleSMTPSSLHandler(handlers.SMTPHandler):
    """
    官方的SMTPHandler不支持SMTP_SSL的邮箱，这个可以两个都支持,并且支持邮件发送频率限制
    """

    def __init__(self, mailhost, fromaddr, toaddrs: tuple, subject,
                 credentials=None, secure=None, timeout=5.0, is_use_ssl=True, mail_time_interval=0):
        """

        :param mailhost:
        :param fromaddr:
        :param toaddrs:
        :param subject:
        :param credentials:
        :param secure:
        :param timeout:
        :param is_use_ssl:
        :param mail_time_interval: 发邮件的时间间隔，可以控制日志邮件的发送频率，为0不进行频率限制控制，如果为60，代表1分钟内最多发送一次邮件
        """
        super().__init__(mailhost, fromaddr, toaddrs, subject,
                         credentials, secure, timeout)
        self._is_use_ssl = is_use_ssl
        self._time_interval = mail_time_interval
        self._msg_map = dict()  # 是一个内容为键时间为值得映射

    def emit(self, record: logging.LogRecord):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        from threading import Thread
        if sys.getsizeof(self._msg_map) > 10 * 1000 * 1000:
            self._msg_map.clear()
        Thread(target=self.__emit, args=(record,)).start()

    def __emit(self, record):
        if record.msg not in self._msg_map or time.time() - self._msg_map[record.msg] > self._time_interval:
            try:
                import smtplib
                from email.message import EmailMessage
                import email.utils
                t_start = time.time()
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self.timeout) if self._is_use_ssl else smtplib.SMTP(self.mailhost, port, timeout=self.timeout)
                msg = EmailMessage()
                msg['From'] = self.fromaddr
                msg['To'] = ','.join(self.toaddrs)
                msg['Subject'] = self.getSubject(record)
                msg['Date'] = email.utils.localtime()
                msg.set_content(self.format(record))
                if self.username:
                    if self.secure is not None:
                        smtp.ehlo()
                        smtp.starttls(*self.secure)
                        smtp.ehlo()
                    smtp.login(self.username, self.password)
                smtp.send_message(msg)
                smtp.quit()
                print(f'[log_manager.py]  发送邮件给 {self.toaddrs} 成功，用时{round(time.time() - t_start,2)} ,发送的内容是--> {record.msg}                    \033[0;35m!!!请去邮箱检查，可能在垃圾邮件中\033[0m')
                self._msg_map[record.msg] = time.time()
            except Exception:
                self.handleError(record)
        else:
            pass
            print(f'[log_manager.py]  邮件发送太频繁，此次不发送这个邮件内容： {record.msg}    ')