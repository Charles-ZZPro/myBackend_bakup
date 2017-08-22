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
import pycurl
import StringIO
import json
reload(sys)  
sys.setdefaultencoding('utf8')  

ssl._create_default_https_context = ssl._create_unverified_context 

mailto_list=["d5n8n0r5v2o7z0q4@tri-pics.slack.com"] 
#mailto_list=["zou.yi@thetripics.com"] 
mail_host="smtp.163.com"  #设置服务器
mail_user="batista19902010"    #用户名
mail_pass="zouyi5764801"   #口令 
mail_postfix="163.com"  #发件箱的后缀

def send_mail_m(to_list,sub,content):  
    me="ip138状态"+"<"+mail_user+"@"+mail_postfix+">"  
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

check_url = "http://api.ip138.com/status/"
ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"

b = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(pycurl.WRITEFUNCTION,b.write)
# c.setopt(pycurl.ENCODING, 'gzip')
c.setopt(pycurl.URL,check_url)
c.setopt(pycurl.HEADER, True)
c.setopt(c.HTTPHEADER, ["Token:0818c205450f205b9c1a815f1b9eb24c"])    
c.setopt(pycurl.USERAGENT, ua)
c.perform()    
value_check_138 = b.getvalue()
b.close()
c.close()

# print(value_check_138)
# print(type(value_check_138))
js_reslut_check138 = value_check_138.split("\r\n")[8]

if js_reslut_check138.count('"ret":"ok"')==0:
	msg = "Oooooooooooops ! ip138 api request error !"
	send_mail_m(mailto_list,'ip138 api return error !!!',msg)
else:
	index_status = js_reslut_check138.find("status")
	index1 = js_reslut_check138.find('"',index_status+1)
	index2 = js_reslut_check138.find('"',index1+1)
	index3 = js_reslut_check138.find('"',index2+2)
	# print(index2)
	# print(index3)
	status = js_reslut_check138[index2+1:index3]
	# print(status)

	if status == "正常":
		index_reqs = js_reslut_check138.find("reqs")
		index_dudu1 = js_reslut_check138.find(":",index_reqs+1)
		index_doudou1 = js_reslut_check138.find(",",index_dudu1+1)
		reqs_forhour = js_reslut_check138[index_dudu1+1:index_doudou1]

		index_hour = js_reslut_check138.find("hour")
		index_dudu2 = js_reslut_check138.find(":",index_hour+1)
		index_doudou2 = js_reslut_check138.find(",",index_dudu2+1)
		max_forhour = js_reslut_check138[index_dudu2+1:index_doudou2]

		index_package = js_reslut_check138.find("package")
		index_dudu3 = js_reslut_check138.find(":",index_package+1)
		index_doudou3 = js_reslut_check138.find("}",index_dudu3+1)
		package = js_reslut_check138[index_dudu3+1:index_doudou3]		

		msg = "status : OK\r\ncurrent requests for hour : " + str(reqs_forhour) + "\r\n" + "current purchase num for hour: " + str(max_forhour) + "\r\n" + "package num : " + str(package) + "\r\n"
        
		if int(reqs_forhour)>=4000:
		    send_mail_m(mailto_list,'ip138 api request count ALERT !!!!!',msg)
		else:
		    # send_mail_m(mailto_list,'ip138接口负载正常',msg)
		    print("OKOKOKOK!!!")

	else:
		msg = "status : " + status + "\r\ntotal msg : " + js_reslut_check138
		send_mail_m(mailto_list,'ip138 api status error !!!!!',msg)

print(msg)
# send_mail_m(mailto_list,'ip138接口负载正常',msg)

 





