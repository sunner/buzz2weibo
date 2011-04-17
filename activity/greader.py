# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

from buzz import BuzzActivity
import re

class GoogleReaderActivity(BuzzActivity):
    
    def setLink(self, activity):
        """从activity取出应发到微博的链接"""

        match = re.search('<a href="(http[^"]+)"', activity['object']['content']);

        self.link = match.group(1)

