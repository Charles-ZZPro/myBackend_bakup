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
import requests
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
    me="leancloud notes"+"<"+mail_user+"@"+mail_postfix+">"  
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

check_url = "https://leancloud.cn/1/statistics/details"
ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"

now = datetime.datetime.now()
date_str = now.strftime('%Y%m%d') 
date_str_hms = now.strftime('%H:%M:%S') 
check_url = check_url + "?from=" + date_str + "&to=" +date_str

b = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(pycurl.WRITEFUNCTION,b.write)
# c.setopt(pycurl.ENCODING, 'gzip')
c.setopt(pycurl.URL,check_url)
c.setopt(pycurl.HEADER, True)
header = ["Referer:https://leancloud.cn/dashboard/apistat.html?appid=Fhdcn0x7iznoVTkg6kzthl6w-gzGzoHsz","X-AVOSCloud-Application-Id:Fhdcn0x7iznoVTkg6kzthl6w-gzGzoHsz","X-AVOSCloud-Application-Key:cTNJGjdsCK6snzqmNhTsumjp","X-XSRF-TOKEN:e8cd528fa131881e51b29e5b01933b1c6f92f1abcd9a36347cb060ddcde2a4b0"]
c.setopt(c.HTTPHEADER, header)    
c.setopt(pycurl.USERAGENT, ua)
c.perform()    
value_check_leancloud = b.getvalue()
b.close()
c.close()

js_reslut_leancloud = value_check_leancloud.split("\r\n")[11]
result_num = js_reslut_leancloud[12:16]

msg = "Today's request count up to now (" + date_str_hms + ") : " + str(result_num)

if int(result_num) >= 24000:
    send_mail_m(mailto_list,'leancloud request count report ALERT !!!',msg)
# else:
#     send_mail_m(mailto_list,'leancloud request count OK',msg)    

# # text_result = "今日leancloud请求数 : " + str(result_num)
# text_result = "leancloud request num : " + str(result_num)

# print(text_result)

# # test_data = {"username": "来自leancloud的提示","text": text_result}
# test_data = {"username": "leancloud notes","text": "request num : 2060"}
# test_data_urlencode = urllib.urlencode(test_data)

# requrl = "https://hooks.slack.com/services/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"
# r = requests.post(requrl, data=test_data)
# print(r.text)

# req = urllib2.Request(url = requrl,data =test_data_urlencode)
# print(req)
# res_data = urllib2.urlopen(req)
# res = res_data.read()
# print(res)


