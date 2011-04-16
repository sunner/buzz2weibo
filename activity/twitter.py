# vim: set fileencoding=utf-8 :

from buzz import BuzzActivity

class TwitterActivity(BuzzActivity):
    """处理来自Twitter的activity"""
    
    def setLink(self, activity):
        """不需要转发到twitter的链接"""
