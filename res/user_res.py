from flask_restful import Resource, reqparse
import mlab
from model.user import User
from mongoengine import *
from model.food import *
from model.oder import *
from operator import itemgetter





class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        parser.add_argument(name="token", type=str, location="json")
        body = parser.parse_args()
        id_user = body.id
        token = body.token
        old_user = User.objects(id_user=id_user).first()
        if old_user is not None:
            return old_user.get_id(), 202
        user = None
        if token is None:
            user = User(id_user=id_user, total_spend=0)
        else:
            user = User(id_user=id_user, total_spend=0, token=token)
        user.save()
        add_user = User.objects().with_id(user.id)
        return add_user.get_id(), 200


class TokenRes(Resource):
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="token", type=str, location="json")
        body = parser.parse_args()
        token = body.token
        user = User.objects().with_id(id)
        user.update(set__token=token)
        return {"message": "OK"}

    def get(self, id):
        user = User.objects().with_id(id)
        return {"token": user.token}


class UserThanThiet(Resource):
    def get(self):
        users = User.objects()
        newlist = sorted(users, key=itemgetter('total_spend'), reverse=True)
        newlist = newlist[:10]
        return [item.get_json() for item in newlist]


class UserRanking(Resource):
    def get(self, id):
        user = User.objects().with_id(id)
        users = User.objects()
        newlist = sorted(users, key=itemgetter('total_spend'), reverse=True)
        pos = list(newlist).index(user)
        rank = str(pos + 1) + "/" + str(len(newlist))
        if pos == 0:
            return {"message": rank + " thành viên ",
                    "rank": (pos + 1),
                    "name": user.name}, 200
        money = (newlist[pos - 1].total_spend - user.total_spend)
        if money == 0:
            money = 1000
        if (pos > 0):
            return {
                       "message": rank + " thành viên " + "bạn cần " + str(
                           abs(money)) + " VND để vượt qua đối thủ tiếp theo!",
                       "rank": (pos + 1),
                       "name": user.name
                   }, 200
        else:
            return {"message": "không có"}, 401


class UserUpdate(Resource):
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="address", type=str, location="json")
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="phone_number", type=str, location="json")
        parser.add_argument(name="urlPic", type=str, location="json")
        parser.add_argument(name="urlFb", type=str, location="json")
        body = parser.parse_args()
        address = body.address
        name = body.name
        if name is None:
            name = "Khách vãng lai"
        phone_number = body.phone_number
        urlPic = body.urlPic
        urlFb = body.urlFb
        user = User.objects().with_id(id)
        user.update(address=address, name=name, phone_number=phone_number, urlPic=urlPic, urlFb=urlFb)
        edit_user = User.objects().with_id(id)
        return mlab.item2json(edit_user), 200

    def get(self, id):
        user = User.objects().with_id(id)
        return mlab.item2json(user), 200


class UserFoodLike(Resource):
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        body = parser.parse_args()
        id_food = body["id"]
        food = Food.objects().with_id(id_food)
        user = User.objects.with_id(id)
        foods = list(user.foods_like)
        for fo in foods:
            if fo == food:
                return {"message": "có rồi add cc đm"}, 401
        foods.append(food)
        user.update(set__foods_like=foods)
        return {"message": "ok"}, 200

    def get(self, id):
        user = User.objects().with_id(id)
        return [food.get_json() for food in user.foods_like]

    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        body = parser.parse_args()
        id_food = body.id
        food = Food.objects().with_id(id_food)
        user = User.objects().with_id(id)
        foods = list(user.foods_like)
        foods.remove(food)
        user.update(set__foods_like=foods)
        return {"message": "ok"}, 200


class UserOrderVerify(Resource):
    def get(self, id):
        user = User.objects().with_id(id)
        orders = Oder.objects(user=user, is_Succues=False)
        return [order.get_json() for order in orders], 200


class UserOrderSuccess(Resource):
    def get(self, id):
        user = User.objects().with_id(id)
        orders = Oder.objects(user=user, is_Succues=True)
        return [order.get_json() for order in orders], 200


class UserSpend(Resource):
    def get(self, id):
        user = User.objects().with_id(id)
        return {"total_spend": str(user.total_spend)}
