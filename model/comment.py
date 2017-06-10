from mongoengine  import *
import mlab
from model.user import *
from model.food import *


class Comment(Document):
    user=ReferenceField("User")
    message=StringField()
    food=ReferenceField("Food")
    date=StringField()

    def get_json(self):

        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "id_comment":oid,
            "user":self.user.get_json(),
            "message":self.message,
            "food":self.food.get_json(),
            "date":self.date
        }