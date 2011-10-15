# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

# 处理Google+消息

import re
import htmllib
import urllib

class GooglePlusActivity(object):
    
    link = ''
    geo = ''
    content = ''
    image = ''
    image_filename = ''
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

        # t.cn只支持http
        self.link = self.https2http(self.link)

        # 将链接中特殊字符及中文转为%XX的形式
        self.link = urllib.quote(self.link)


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

        # 取链接里的文本，如果有的话
        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['objectType'] == 'article':
                    self.content += ' ' + attach['displayName']



    def setGeo(self, activity):
        """从activity取出经纬坐标"""

        if activity.has_key('geocode'):
            self.geo = activity['geocode']


    def setImage(self, activity):
        """从activity取出应发到微博的图片地址"""

        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['objectType'] == 'photo':
                    image = attach['fullImage']
                    self.image = self.https2http(image['url'])

                    if image.has_key('content'):
                        self.image_filename = attach['content']
                    else:
                        # 从type里取扩展名
                        self.image_filename = 'tempname.' + image['type'].split('/')[-1]

                    break;  # 只留第一个图 TODO: 合并多个图


    def setOriginLink(self, activity):
        """从activity取出到g+的链接"""

        # t.cn只支持http
        self.origin_link = self.https2http(activity['url'])

    def unescape(self, s):
        """解码html转义"""

        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()

    def encode(self, codeset):
        """转换成员变量字符集"""

        self.link           = self.link.encode(codeset)
        self.geo            = self.geo.encode(codeset)
        self.content        = self.content.encode(codeset)
        self.image          = self.image.encode(codeset)
        self.image_filename = self.image_filename.encode(codeset)
        self.id             = self.id.encode(codeset)
        self.origin_link    = self.origin_link.encode(codeset)

    def https2http(self, httpslink):
        """将https链接转为http链接"""

        return httpslink.replace('https://', 'http://', 1)

