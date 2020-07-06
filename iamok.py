#_*_coding: utf-8 _*_
import time
import requests
import re
import os
import execjs
# import http.cookiejar as cj

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
# }

#iamok文件夹所在路径
iamok_path = '/home/aiyolo/iamok'
#账户信息
user = os.environ["scut_username"]
passwd = os.environ["scut_password"]

#创建session
session = requests.Session()
# session.cookies = cj.LWPCookieJar()

#登陆页面，
url_1 = 'https://sso.scut.edu.cn/cas/login?service=https%3A%2F%2Fiamok.scut.edu.cn%2Fcas%2Flogin'

#利用des.js文件加密，得到登陆表单数据rsa
r = session.get(url_1)
lt = re.findall('name="lt" value="(.*?)"', r.text)[0]
execution = re.findall('name="execution" value="(.*?)"', r.text)[0]

with open(os.path.join(iamok_path,'des.js')) as f:
    ctx = execjs.compile(f.read())
string1 = user + passwd + lt
rsa = ctx.call('strEnc', string1, '1', '2', '3')

#登陆所需的表单数据
login_data = {
    'rsa': rsa,
    'ul': len(user),
    'pl': len(passwd),
    'lt': lt,
    'execution': execution,
    '_eventId': 'submit'
}
##进行登陆登陆
session.post(url_1, data=login_data)

#optional，保存cookie到本地
# session.cookies.save('cookie.txt', ignore_discard=True, ignore_expires=True)

#get请求链接，解析你的健康数据
url_2 = 'https://iamok.scut.edu.cn/mobile/recordPerDay/getRecordPerDay'
html = session.get(url_2)
submit_data = html.json()['data']

#post请求链接，提交新的健康数据
url_3 = 'https://iamok.scut.edu.cn/mobile/recordPerDay/submitRecordPerDay'
output = session.post(url_3, json=submit_data)
print(output.text)


#载入本地cookie
# s = requests.session()
# s.cookies = cj.LWPCookieJar(filename='cookies.txt')
# s.cookies.load(filename='cookies.txt', ignore_discard=True)

