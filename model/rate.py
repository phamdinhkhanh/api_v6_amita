from mongoengine import *
from model.food import Food
import mlab
from model.user import *


class RateFood(Document):
    food=ReferenceField("Food")
    users=ListField(ReferenceField("User"))

    def get_json(self):
        return {
            "food":self.food.get_json(),
            "users":[item.get_json() for item in self.users]
        }


