#!/usr/bin/python
# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

from config import *
from urllib2 import urlopen, URLError
from json import load
from activity import *
from weibopy.auth import OAuthHandler
from weibopy.api import API
from weibopy.error import WeibopError
from time import sleep
import os, errno, sys
import Image

WEIBO_APP_KEY = '3127127763'
WEIBO_APP_SECRET = '21cc35f55fc8fe73b73162964c0bb415'

# 运行一次最多同步几条。缺省3。连续同步太多会被休息的
WEIBO_MAX_SYNC_COUNT = 3

'''Concatenate multiply images as one from top to down'''
def catimages(image_files):

    if len(image_files) <= 1:
        return image_files[0]

    images = []
    max_width = 0

    '''Load images and get the max width'''
    for f in image_files:
        img = Image.open(f)
        images.append(img)

        width, height = img.size
        if width > max_width:
            max_width = width

    '''resize all images to max_width'''
    total_height = 0
    resized_images = []
    for img in images:
        width, height = img.size
        new_height = max_width / width * height
        resized_images.append(img.resize((max_width, new_height)))
        total_height = total_height + new_height

    '''concatenate them'''
    result_img = Image.new('RGB', (max_width, total_height))
    ypos = 0
    for img in resized_images:
        result_img.paste(img, (0, ypos))
        ypos = ypos + img.size[1]

    imagefile = IMAGES_PATH + '/' + 'final.jpg'
    result_img.save(imagefile)
    return imagefile

def post2weibo(api, act):
    
    message = act.content + ' ' + act.link
    if APPEND_SHARE_FROM_BUZZ_LINK:
        message += u' //转发自%s'.encode('utf-8') % act.origin_link

    imagefiles = []
    for image in act.images:
        # 下载图像文件
        try:
            u = urlopen(image.url);
            data = u.read()
            u.close()
        except URLError:
            # 如果下载不下来，表示……，就别试了，当普通消息发吧
            pass
        else:
            filename = IMAGES_PATH + '/' + image.filename
            f = open(filename, 'w')
            f.write(data)
            f.close()
            imagefiles.append(filename)

    if len(imagefiles) > 0:
        imagefile = catimages(imagefiles)

    while (True):
        try:
            if len(imagefiles) > 0:
                api.upload(imagefile, status=message, lat=act.geo[0], long=act.geo[1])
            else:
                api.update_status(status=message, lat=act.geo[0], long=act.geo[1])
        except WeibopError, e:
            if e.reason.find('error_code:400,40013:Error:') == 0:
                # 微博太长，剪裁且留原始链接。原始链接不会太长，所以不会死循环
                message = unicode(message, 'utf-8')[0:80] + u'....更多:'
                message = message.encode('utf-8') + act.origin_link
                print '内容过长，截断发表:'
                print message
            else:
                raise
        else:
            break

    return True

# 测试config.py文件是否存在

if not os.path.exists(sys.path[0] + os.sep + 'config.py'):
    print '找不到配置文件。请先运行setup.py'
    sys.exit(1)

# 建图片目录
try:
    os.makedirs(IMAGES_PATH)
except OSError, e:
    if e.errno == errno.EEXIST:
        pass
    else:
        raise

buzz_url = 'https://www.googleapis.com/plus/v1/people/' + BUZZ_USERID + '/activities/public?key=' + GOOGLE_API_KEY

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
except IOError, e:
    # 如果文件不存在，就继续；否则，触发异常
    if e.errno != errno.ENOENT:
        raise

# 开始同步
count = 0
items = buzz['items']
items.reverse()  # Buzz是后发的在前，所以翻转一下。感谢王瑞珩的建议
for item in items:

    act = GooglePlusActivity(item);

    # 同步未同步过的
    if act.id not in synced_ids:
        print '-----------------------'
        print 'syncing ' + act.id
        print act.origin_link
        if act.content != '':
            print act.content
        if act.link != '':
            print act.link
        for image in act.images:
            print image.url
        if act.geo != '':
            print act.geo

        if DEBUG:
            continue

        if post2weibo(api, act):
            synced_ids.add(act.id)

            # 将同步过的activity id写入历史文件
            fp = open(HISTORY_FILE, 'w')
            for id in synced_ids:
                fp.write(id + '\n')
            fp.close()

            count = count + 1
            if count >= WEIBO_MAX_SYNC_COUNT:
                break

            sleep(1)  # 延时才能让新浪微博按正确顺序显示
