#!/usr/bin/python
# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

from weibo import APIClient
from urllib2 import urlopen, URLError, HTTPError
from json import load
import sys, os
import codecs

if os.path.isfile('config.py'):
    from config import *
else:
    GOOGLE_API_KEY = ''
    BUZZ_USERID = ''
    WEIBO_TOKEN = ''
    WEIBO_TOKEN_EXPIRES = ''
    USE_HTTPS = u'True  # Google+ API只支持https'
    HISTORY_FILE = sys.path[0] + os.sep + '.buzz2weibo_history'
    IMAGES_PATH = '/tmp/buzz2weibo'
    DEBUG = 'False'
    APPEND_SHARE_FROM_BUZZ_LINK = 'False'


WEIBO_APP_KEY = '3127127763'
WEIBO_APP_SECRET = '21cc35f55fc8fe73b73162964c0bb415'

def default_input(prompt, default):
    if len(default) != 0:
        prompt = prompt + '(回车使用上次配置"' + default +'")'
    input = raw_input(prompt + ':').strip()
    if len(input) == 0:
        return default
    else:
        return input

print '''欢迎使用buzz2weibo配置向导！
===========================
本向导会使用您输入的数据，在当前目录创建config.py文件。 '''

print '''
---------------------------
Google+的API单个KEY每日只能请求1000次。所以您必须申请一个自己的Google API Key
请访问 https://code.google.com/apis/console/ ，
然后Create Project，Enable Google+ API，再转到API Access页面，
Simple API Access中的API key就是你要得到的。拷贝粘贴到下面。
'''

GOOGLE_API_KEY = default_input('请输入Google API key', GOOGLE_API_KEY)

print '''
---------------------------
为了获得您的Google用户ID，请访问 https://plus.google.com/me
登录后，地址栏会变成类似这样：
https://plus.google.com/106019261651260565998/posts
其中最长的那串纯数字，就是您的Google用户ID
'''
BUZZ_USERID = default_input('请输入Google用户ID', BUZZ_USERID).strip()

print '''
---------------------------
正在验证Google API key和用户ID...'''
people_url = 'https://www.googleapis.com/plus/v1/people/' + BUZZ_USERID + '?key=' + GOOGLE_API_KEY
fp = urlopen(people_url)
people = load(fp)
fp.close()
yn = raw_input('您在Google+的名字是“%s”吗？(Y/N)：' % people['displayName'].encode('utf-8')).strip()

if yn[0].lower() != 'y':
    print '''请重新运行本向导，输入正确的BuzzID。'''
    sys.exit(1)

# OAuth 2.0 begins

auth = APIClient(WEIBO_APP_KEY, WEIBO_APP_SECRET, 'https://api.weibo.com/oauth2/default.html')
auth_url = auth.get_authorize_url()
print ''
print '请在浏览器中访问下面链接，授权给buzz2weibo后，会在跳转到的页面url中code参数后面看到授权码'
print ''
print auth_url
print ''

while True:
    verifier = raw_input('请输入授权码：').strip()
    try:
        token = auth.request_access_token(verifier)
    except HTTPError:
        print '授权码不正确或者过期，请重新运行本向导'
        sys.exit(1)
    else:
        break

WEIBO_TOKEN = token.access_token
WEIBO_TOKEN_EXPIRES = token.expires_in

# Generate config.py
config = u'''# vim: set fileencoding=utf-8 :

# Google API key
GOOGLE_API_KEY = '%s'

# 用户参数
BUZZ_USERID = '%s'
WEIBO_TOKEN = '%s'
WEIBO_TOKEN_EXPIRES = '%s'

# 是否使用https连接google
USE_HTTPS = %s

# 保存同步历史的文件路径
HISTORY_FILE = '%s'

# 下载然后传到微博的图片临时存放目录
IMAGES_PATH = '%s'

# 调试模式下，不会真的发微博，只打印状态
DEBUG = %s

# 是否附带buzz链接
APPEND_SHARE_FROM_BUZZ_LINK = %s
''' % (GOOGLE_API_KEY,
       BUZZ_USERID,
       WEIBO_TOKEN,
       WEIBO_TOKEN_EXPIRES,
       USE_HTTPS,
       HISTORY_FILE,
       IMAGES_PATH,
       DEBUG,
       APPEND_SHARE_FROM_BUZZ_LINK)


fp = codecs.open('config.py', 'w', 'utf-8')
fp.write(config)
fp.close()

print ''
print 'config.py生成完毕，运行buzz2weibo.py开始同步。编辑config.py可以做更多个性化设置'
