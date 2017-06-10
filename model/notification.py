from mongoengine import *
import mlab


class Notification(Document):
    message_title = StringField()
    message_body = StringField()
    datetime = StringField()
    is_read = BooleanField()
    def get_json(self):
        return mlab.item2json(Notification.objects().with_id(self.id))
