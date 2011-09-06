# vim: set fileencoding=utf-8 :

# buzz2weibo
# Copyright 2011 Liu Wenmao 
# See LICENSE for details.

from buzz import BuzzActivity

class FlickrActivity(BuzzActivity):
    """处理来自Flickr的activity"""
    
    def setImage(self, activity):
        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['type'] == 'photo':
                    self.image = "http://images0-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&gadget=a&resize_h=500&url="+self.https2http(attach['links']['enclosure'][0]['href'])
                    #self.image = self.https2http(attach['links']['enclosure'][0]['href'])
                    self.image_filename = self.image.split('/')[-1][-10:]
                    self.content += " " + attach['title']
                    if not self.image_filename.lower().endswith('.jpg') and \
                       not self.image_filename.lower().endswith('.jpeg') and \
                       not self.image_filename.lower().endswith('.png') and \
                       not self.image_filename.lower().endswith('.gif'):
                            # 先不管三七二一，都当jpg吧
                            self.image_filename += '.jpg'
                    break;  # 只留第一个图

    def setContent(self, activity):
#        super(FlickrActivity, self).setContent(activity)
        if self.content != '':
            self.content = u'我上传了一批图片: %s ' % self.content

    def setLink(self, activity):
        super(FlickrActivity, self).setLink(activity)

        if activity['object'].has_key('attachments'):
            for attach in activity['object']['attachments']:
                if attach['type'] == 'photo' and attach['links']['alternate'][0]['href']!="":
                    self.link = attach['links']['alternate'][0]['href']
                    break

