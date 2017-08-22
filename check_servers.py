#-*-coding:utf-8-*-
from __future__ import print_function
from __future__ import unicode_literals
import gzip 
import tarfile
import os
from django.db import models
import psycopg2
import sys
import datetime
import random
import shutil
import socket
import time
import oss2
from django.http import StreamingHttpResponse
import os, tempfile, zipfile  
from django.http import HttpResponse  
# from django.core.servers.basehttp import FileWrapper  
from wsgiref.util import FileWrapper
import urllib2
import urllib
from django.http import HttpResponseRedirect 
import ssl
import smtplib
from email.mime.text import MIMEText
from email.header import Header
ssl._create_default_https_context = ssl._create_unverified_context 

# mailto_list=["d5n8n0r5v2o7z0q4@tri-pics.slack.com"] 
mailto_list=["zou.yi@thetripics.com"] 
mail_host="smtp.163.com"  #设置服务器
mail_user="batista19902010"    #用户名
mail_pass="zouyi5764801"   #口令 
mail_postfix="163.com"  #发件箱的后缀
  
def send_mail_m(to_list,sub,content):  
    me="Unfortunately ..."+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = Header(sub, 'utf-8')  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print(str(e))
        return False   


ops = "https://ops.thetripics.com"
yt = "https://yt.thetripics.com/index.html"
ad_url = "https://url.thetripics.com/595dc2288d6d81005718daf0"
wallpaper = "https://wallpaper.thetripics.com/test_html.html"
ad_static_oss = "https://adcdn-oss.thetripics.com/test_html.html"
apk_oss= "https://apk.thetripics.com/test_apk.apk"
apk_internal_oss = "https://apk-internal.thetripics.com/test_apk.apk"
apis = "https://apis.thetripics.com:8098/"

url_cols = [ops,yt,ad_url,wallpaper,ad_static_oss,apk_oss,apk_internal_oss,apis]

issue_urls = []

got_issue = False

for every_url in url_cols:
	# print(every_url)
	try:
		status = urllib.urlopen(every_url).code
		print(every_url+"   status:"+str(status))
	except:
		status = 886

	if status != 200:
		got_issue = True
		issue_urls.append(every_url)


if got_issue==True:
    mail_content = "Dead server address : \r\n"
    for every_issue in issue_urls:
    	mail_content = mail_content + every_issue + " \r\n"

	send_mail_m(mailto_list,'ALERT !!! SERVER DOWN !!!',mail_content)
	# sender = 'batista19902010@163.com'
	# receivers = ['d5n8n0r5v2o7z0q4@tri-pics.slack.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
	 
	# # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
	# message = MIMEText(mail_content, 'plain', 'utf-8')
	# message['From'] = Header("真的挂了", 'utf-8')
	# message['To'] =  Header("阿西巴", 'utf-8')
	 
	# subject = '完了，服务器挂了'
	# message['Subject'] = Header(subject, 'utf-8')
	 
	 
	# try:
	#     smtpObj = smtplib.SMTP('smtp.163.com')
	#     smtpObj.sendmail(sender, receivers, message.as_string())
	#     print("邮件发送成功")
	# except smtplib.SMTPException:
	#     print("Error: 无法发送邮件")

