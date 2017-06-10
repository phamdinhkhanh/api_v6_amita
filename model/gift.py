from mongoengine import *
import mlab

class GiftCode(Document):
    code=StringField()
    use_number=IntField()
    spend_min=FloatField()
    price=FloatField()

    def to_json(self):
        return {"code":self.code,
                "use_number":self.use_number,
                "spend_min":self.spend_min,
                "price":self.price
                }