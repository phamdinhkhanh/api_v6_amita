from mongoengine import Document, StringField
from flask_restful import Resource, reqparse
import mlab
from model.food import *
from model.user import *
from model.rate import *


class FoodRes(Resource):
    def get(self):
        food = Food.objects()
        return mlab.list2json(food), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="url", type=str, location="json")
        parser.add_argument(name="coint_old", type=str, location="json")
        parser.add_argument(name="coint_new", type=str, location="json")
        body = parser.parse_args()
        name = body.name
        url = body.url
        coint_old = body.coint_old
        coint_new = body.coint_new
        try:
            old = float(coint_old)
            new = float(coint_new)
        except:
            return {"message": "post cái lol gì? giá là số ok? bỏ chữ Đ hay VND đi"}, 401
        cout_rate = 0
        rate = 5
        if name is None or url is None or coint_new is None or coint_old is None:
            return {"message": "Gửi cc thiếu trường đcm"}, 401
        food = Food(name=name, url=url, coint_new=coint_new, coint_old=coint_old, cout_rate=cout_rate, rate=rate)
        food.save()
        add_food = Food.objects().with_id(food.id)
        return mlab.item2json(add_food), 200


class FoodRate(Resource):
    def put(self, id):
        food = Food.objects().with_id(id)

        parser = reqparse.RequestParser()
        parser.add_argument(name="id_user", type=str, location="json")
        parser.add_argument(name="star", type=float, location="json")
        body = parser.parse_args()
        id_user=body["id_user"]
        star=body["star"]
        if id_user is None or star<0 or star>5:
            return {"message":"Gửi cc gì đấy!"}
        rate_food = RateFood.objects(food=food).first()
        if rate_food is None:
            users=[]
            users.append(User.objects().with_id(id_user))
            rate_food = RateFood(food=food, users=users)
            rate_food.save()
            cout_rate=food.cout_rate
            rate=food.rate
            new_rate=((rate*cout_rate)+star)/(cout_rate+1)
            food.update(set__rate=new_rate,set__cout_rate=cout_rate+1)
            return {"message":"OK"},200
        else:
            users=rate_food.users
            user=User.objects().with_id(id_user)
            if user in users:
                return {"message":"rate rồi đm"},400
            else:
                cout_rate = food.cout_rate
                rate = food.rate
                new_rate = ((rate * cout_rate) + star) / (cout_rate + 1)
                food.update(set__rate=new_rate, set__cout_rate=cout_rate + 1)
                users.append(user)
                rate_food.update(set__users=users)
                return {"message":"Ok"},200

class FoodGetHotSales(Resource):
    def get(self):
        listFood = []
        foods = Food.objects()
        for food in foods:
            if (float(food.coint_old) - float(food.coint_new)) > 0:
                listFood.append(food)

        return [foo.get_json() for foo in listFood]


class FoodFavorite(Resource):
    def get(self):
        foods = Food.objects(is_favorite=True)
        return [food.get_json() for food in foods]


class FoodLike(Resource):
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
        return {"message": "ok"}, 200


class FoodInfoRes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        parser.add_argument(name="info", type=str, location="json")
        body = parser.parse_args()

        id = body["id"]
        info = body["info"]

        food = Food.objects.with_id(id)
        food_infor = FoodInfo(food=food, info=info)
        return food_infor.get_json()


class FoodInfoGetRes(Resource):
    def get(self, id):
        foodInfor = FoodInfo.objects().with_id(id)
        return foodInfor.get_json()


class GetCover(Resource):
    def get(self):
        return {
            "url": "http://res.cloudinary.com/dumfykuvl/image/upload/v1492246766/back_2_bqh7tm.png"}
