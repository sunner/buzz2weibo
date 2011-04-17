#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from config import *
from urllib2 import urlopen, URLError
from json import load
from activity import *
from weibopy.auth import OAuthHandler
from weibopy.api import API
import os, errno

WEIBO_APP_KEY = '3127127763'
WEIBO_APP_SECRET = '21cc35f55fc8fe73b73162964c0bb415'

# 运行一次最多同步几条。缺省3。连续同步太多会被休息的
WEIBO_MAX_SYNC_COUNT = 3

def post2weibo(api, act):
    
    message = act.content + act.link
    if act.geo != '':
        geo = act.geo.split(' ')
    else:
        geo = [None, None]

    if act.image != '':

        # 下载图像文件
        try:
            u = urlopen(act.image);
            data = u.read()
            u.close()
        except URLError:
            # 如果下载不下来，表示……，就别试了，当普通消息发吧
            raise
            status = api.update_status(status=message, lat=geo[0], long=geo[1])
            return

        filename = IMAGES_PATH + '/' + act.image_filename
        f = open(filename, 'w')
        f.write(data)
        f.close()

        status = api.upload(filename, status=message, lat=geo[0], long=geo[1])
    else:
        status = api.update_status(status=message, lat=geo[0], long=geo[1])

# 建图片目录
try:
    os.makedirs(IMAGES_PATH)
except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST:
        pass
    else:
        raise

if USE_HTTPS:
    prefix = 'https://'
else:
    prefix = 'http://'
buzz_url=prefix + 'www.googleapis.com/buzz/v1/activities/' + BUZZ_USERID + '/@public?alt=json'

# 读buzz
fp = urlopen(buzz_url)
#fp = open('buzz.json')
buzz = load(fp)
fp.close()

# 微博认证
auth = OAuthHandler(WEIBO_APP_KEY, WEIBO_APP_SECRET)
auth.setToken(WEIBO_TOKEN_KEY, WEIBO_TOKEN_SECRET)
api = API(auth)


# 读已经同步过的activity id
synced_ids = set()
try:
    fp = open(HISTORY_FILE, 'r')
    for line in fp:
        synced_ids.add(line.strip())
    fp.close()
except IOError  as (errno, strerror):
    # 如果文件不存在，就继续；否则，触发异常
    if errno != 2:
        raise

# 开始同步
count = 0
for item in buzz['data']['items']:

    # 解析buzz
    try:
        act = eval(item['source']['title'].replace(' ', '') + 'Activity(item)')
    except NameError:
        # use WildcardActivity as default
        act = WildcardActivity(item);

    # 同步未同步过的
    if act.id not in synced_ids:
        print '-----------------------'
        print 'syncing ' + act.id
        print item['source']['title']
        if act.content != '':
            print act.content
        if act.link != '':
            print act.link
        if act.image != '':
            print act.image
        if act.image_filename != '':
            print act.image_filename
        if act.geo != '':
            print act.geo

        if not DEBUG:

            post2weibo(api, act)
            synced_ids.add(act.id)

            # 将同步过的activity id写入历史文件
            fp = open(HISTORY_FILE, 'w')
            for id in synced_ids:
                fp.write(id + '\n')
            fp.close()

    count = count + 1
    if count >= WEIBO_MAX_SYNC_COUNT:
        break
