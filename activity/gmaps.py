# vim: set fileencoding=utf-8 :

from buzz import BuzzActivity

class GoogleMapsformobileActivity(BuzzActivity):
    """post from google maps for android"""

    def setImage(self, activity):
        super(GoogleMapsformobileActivity, self).setImage(activity)
        self.image_filename += '.jpg'

