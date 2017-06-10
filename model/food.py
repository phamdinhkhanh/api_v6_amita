from mongoengine import *
import mlab


class Food(Document):
    name = StringField()
    url = StringField()
    coint_old = StringField()
    coint_new = StringField()
    cout_rate = IntField()
    rate = FloatField()
    is_favorite=BooleanField()

    def get_json(self):
        return mlab.item2json(self)
        # nếu đánh giá thêm 1 lần = rate*cout_rate +đánh giá chia (count_rate+1)


class FoodInfo(Document):
    food=ReferenceField("Food")
    info=StringField()

    def get_json(self):
        return {
            "food":self.food.get_json(),
            "info":self.info
        }