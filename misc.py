# -*- coding:cp936 -*-
import win32api 
import win32con
import os 
import time 

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def sendMail():
    
    #����һ����������ʵ��
    msg = MIMEMultipart()
    
    #���츽��1
    att1 = MIMEText(open(r'D:\backup\backup.py', 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="backup.zip"'#�����filename��������д��дʲô���֣��ʼ�����ʾʲô����
    msg.attach(att1)
    
    #���ʼ�ͷ
    msg['to'] = 'xudi1989@ruc.edu.cn'
    msg['from'] = 'ycyjxudi1989@126.com'
    msg['subject'] = 'Auto Backup'
    #�����ʼ�
    try:
        server = smtplib.SMTP()
        server.connect('smtp.126.com')
        server.login('ycyjxudi1989','')#XXXΪ�û�����XXXXXΪ����
        server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.quit()
        print '���ͳɹ�'
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