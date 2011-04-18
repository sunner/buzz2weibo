# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

# 每条Buzz的基类。
# 如果要对某种来源做特别处理，需要继承此类。
# 例如来源是Google Reader，就派生一个GoogleReaderActivity

import re
import htmllib

class BuzzActivity(object):
    
    link = ''
    geo = ''
    content = ''
    image = ''
    image_filename = ''
    id = ''

    def __init__(self, activity):

        self.setID(activity)
        self.setLink(activity)
        self.setContent(activity)
        self.setGeo(activity)
        self.setImage(activity)

        # 不用utf-8，weibopy罢工，命令行重定向之类也出错
        self.encode('utf-8')


    def setID(self, activity):
        """从activity取出ID"""

        self.id = activity['id']


    def setLink(self, activity):
        """从activity取出应发到微博的链接"""

        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['type'] == 'article':
                    self.link = attach['links']['alternate'][0]['href']

    
    def setContent(self, activity):
        """从activity取出应发到微博的文字内容"""

        # 去掉所有html tag
        self.content = self.unescape(re.sub('<[^<]+?>', '', activity['object']['content']))

        # 取链接里的文本
        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['type'] == 'article':
                    self.content += ' ' + attach['content']



    def setGeo(self, activity):
        """从activity取出经纬坐标"""

        if activity.has_key('geocode'):
            self.geo = activity['geocode']


    def setImage(self, activity):
        """从activity取出应发到微博的图片地址"""

        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['type'] == 'photo':
                    self.image = attach['links']['enclosure'][0]['href']
        self.image_filename = self.image.split('/')[-1]


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
