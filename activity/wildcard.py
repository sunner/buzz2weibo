# vim: set fileencoding=utf-8 :

from buzz import BuzzActivity

class WildcardActivity(BuzzActivity):
    """处理来自非常见源的activity"""
    
    def setLink(self, activity):
        """从activity取出应发到微博的链接"""

        if activity.has_key('crosspostSource'):
            self.link = activity['crosspostSource']
