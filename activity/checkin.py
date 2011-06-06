# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

from buzz import BuzzActivity

class GoogleLatitudeCheckinActivity(BuzzActivity):
    """Google Latitude Check-in post"""

    def setContent(self, activity):
        self.content = u'我现在在这里'
