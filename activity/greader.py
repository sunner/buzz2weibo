# vim: set fileencoding=utf-8 :

from buzz import BuzzActivity
import re

class GoogleReaderActivity(BuzzActivity):
    
    def setLink(self, activity):
        """从activity取出应发到微博的链接"""

        match = re.search('<a href="(http[^"]+)"', activity['object']['content']);

        self.link = match.group(1)

