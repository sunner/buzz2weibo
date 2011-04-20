# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Sun Zhigang
# See LICENSE for details.

from buzz import BuzzActivity

class GoogleMapsformobileActivity(BuzzActivity):
    """post from google maps for android"""

    def setImage(self, activity):
        super(GoogleMapsformobileActivity, self).setImage(activity)
        if self.image != '':
            self.image = self.https2http(self.image)
            self.image_filename += '.jpg'

