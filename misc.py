# -*- coding:cp936 -*-
import win32api 
import win32con
import os 
import time 

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def sendMail():
    
    #创建一个带附件的实例
    msg = MIMEMultipart()
    
    #构造附件1
    att1 = MIMEText(open(r'D:\backup\backup.py', 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="backup.zip"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)
    
    #加邮件头
    msg['to'] = 'xudi1989@ruc.edu.cn'
    msg['from'] = 'ycyjxudi1989@126.com'
    msg['subject'] = 'Auto Backup'
    #发送邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.126.com')
        server.login('ycyjxudi1989','')#XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.quit()
        print '发送成功'
    except Exception, e:  
        print str(e) 
def update_system_time():
    c = ntplib.NTPClient() 
    response = c.request('pool.ntp.org') 
    ts = response.tx_time 
    _date = time.strftime('%Y-%m-%d',time.localtime(ts)) 
    _time = time.strftime('%X',time.localtime(ts)) 
    os.system('date {} && time {}'.format(_date,_time))

win32api.MessageBox(win32con.NULL, 'hi python', 'hi', win32con.MB_OK) 