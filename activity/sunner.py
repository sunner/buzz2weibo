# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

from wildcard import WildcardActivity

class HelloWorldActivity(WildcardActivity):
    """Sunner的博客专用（http://blog.sunner.cn）"""

    def setContent(self, activity):
        super(HelloWorldActivity, self).setContent(activity)
        if self.content != '':
            self.content = u'我写了篇新博客《%s》 ' % self.content

