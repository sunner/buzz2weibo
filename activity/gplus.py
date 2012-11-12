# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

# 处理Google+消息

import re
import htmllib
import hashlib

class gplus_image(object):
    url = ''
    filename = ''

    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

    def encode(self, codeset):
        self.url = self.url.encode(codeset)
        self.filename = self.filename.encode(codeset)
        return self


class GooglePlusActivity(object):
    
    link = ''
    geo = ['0.0', '0.0']
    content = ''
    images = []
    id = ''
    origin_link = ''

    def __init__(self, activity):

        self.setID(activity)
        self.setLink(activity)
        self.setContent(activity)
        self.setGeo(activity)
        self.setImage(activity)
        self.setOriginLink(activity)

        # 不用utf-8，weibopy罢工，命令行重定向之类也出错
        self.encode('utf-8')


    def setID(self, activity):
        """从activity取出ID"""

        self.id = activity['id']


    def setLink(self, activity):
        """从activity取出应发到微博的链接"""

        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['objectType'] == 'article':
                    self.link = attach['url']

    
    def setContent(self, activity):
        """从activity取出应发到微博的文字内容"""

        # 用title做微博内容，并去掉所有html tag
        self.content = self.unescape(re.sub('<[^<]+?>', '', activity['title']))

        # share的post要加上用户自己的话
        if (activity['verb'] == 'share' and activity['annotation'] != ''):
            self.content = activity['annotation'] + ' ' + self.content;

        # 取链接里的文本，如果有的话
        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['objectType'] == 'article':
                    self.content += ' ' + attach['displayName']

    def setGeo(self, activity):
        """从activity取出经纬坐标"""

        if activity.has_key('geocode'):
            self.geo = activity['geocode'].split(' ')
            # 修正天杀的误差
            self.geo[0] = str(float(self.geo[0]) + 0.0019953)
            self.geo[1] = str(float(self.geo[1]) + 0.0059628)


    def setImage(self, activity):
        """从activity取出应发到微博的图片地址"""

        self.images = []

        # Google Reader会把full image的链接设原文链接，所以不能将其上传
        if activity['provider']['title'] == 'Google Reader':
            return

        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['objectType'] == 'photo':
                    image = attach['fullImage']
                    url = self.https2http(image['url'])

                    if image.has_key('content'):
                        filename = attach['content']
                    else:
                        # 从type里取扩展名
                        filename = hashlib.md5(url.encode('UTF-8')).hexdigest() + '.' + image['type'].split('/')[-1]

                    self.images.append(gplus_image(url, filename))


    def setOriginLink(self, activity):
        """从activity取出到g+的链接"""

        self.origin_link = activity['url']

    def unescape(self, s):
        """解码html转义"""

        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()

    def encode(self, codeset):
        """转换成员变量字符集"""

        self.link           = self.link.encode(codeset)
        self.content        = self.content.encode(codeset)
        self.id             = self.id.encode(codeset)
        self.origin_link    = self.origin_link.encode(codeset)
        self.images         = [s.encode(codeset) for s in self.images]

    def https2http(self, httpslink):
        """将https链接转为http链接"""

        return httpslink.replace('https://', 'http://', 1)

