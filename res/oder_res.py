from flask_restful import Resource, reqparse
from model.oder import *
from model.user import User
from model.food import Food
import mlab
from pyfcm.fcm import FCMNotification
import json
import requests
import datetime
from model.gift import *


class OderRes(Resource):
    def get(self):
        oders = Oder.objects(is_Succues=False)
        return [order.get_json() for order in oders], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="items", type=list, location="json")
        parser.add_argument(name="address", type=str, location="json")
        parser.add_argument(name="phone_number", type=str, location="json")
        parser.add_argument(name="user", type=str, location="json")
        parser.add_argument(name="code", type=str, location="json")
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="id", type=str, location="json")
        parser.add_argument(name="count", type=int, location="json")
        body = parser.parse_args()
        items = body["items"]
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        address = body.address
        phone_number = body.phone_number
        user_id = body.user
        name = body.name
        code = body["code"]
        if items is None or date is None or address is None or phone_number is None or user_id is None:
            return {"message": "Thiếu trường "}, 400

        if len(str(phone_number)) > 11 or len(str(phone_number)) < 10:
            return {"message": "Số điện thoại cc gì! sdt 10 or 11 số!"}, 402
        try:
            sdt = float(phone_number)
        except:
            return {"message": "Số điện thoại lol gì mà có chữ?"}, 401
        API_KEY = "AIzaSyCEB4QVng3uFEQ-SwxfwOWAG4H3sr7Mfi8"
        url_request = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=vi-VN&key={2}".format(
            "301 Trường Chinh,Hà nội", str(address) + " Hà Nội", API_KEY)
        ship_spend = 0
        try:
            req = requests.get(url_request)
            json_data = json.loads(req.content)
            list_add = json_data["rows"]
            elements = list_add[0]["elements"]
            km = elements[0]["distance"]["text"]
            txt = str(km).split(" ")
            distance = txt[0].replace(",", ".")
            ship_spend = float(distance) * 3000
        except:
            ship_spend = -1

        order_items = []
        spend = 0
        for item in items:
            food_id = item.id
            count = item.count
            try:
                sl = int(count)
                if sl < 1:
                    return {"message": "Số lượng >0 ok?"}, 401
            except:
                return {"message": "count là số int ok?"}, 401
            food = Food.objects().with_id(food_id)
            single_order = SingleOrder(count=count, food=food)
            order_items.append(single_order)
            spend += (float(food["coint_new"]) * int(count))

        if spend == 0:
            return {"message": "Đặt hàng cc gì mà giá bằng 0?"}, 401
        try:
            user = User.objects().with_id(user_id)
            user.update(address=address, phone_number=phone_number, name=name)
        except:
            return {"message": "Đm gửi cái user id mà data mlab lưu ấy"}, 401
        oder = Oder()
        code = str(code).lower()
        gift = GiftCode.objects(code=code).first()
        try:
            spend_min = gift.spend_min
        except:
            spend_min = -1
        if (spend > 0 and (spend >= spend_min and spend_min != -1)):
            use_number = gift["use_number"]
            use_number -= 1
            if use_number == 0:
                gift.delete()
            else:
                gift.update(set__use_number=use_number)
            oder = Oder(items=order_items, date=date, address=address, phone_number=phone_number,
                        user=User.objects().with_id(user_id),
                        is_Succues=False, spend=spend + ship_spend - gift.price, ship_money=ship_spend,
                        code_price=gift.price,is_Received=False,is_Shipping=False)
        else:
            oder = Oder(items=order_items, date=date, address=address, phone_number=phone_number,
                        user=User.objects().with_id(user_id),
                        is_Succues=False, spend=spend+ship_spend, ship_money=ship_spend, code_price=0,is_Received=False,is_Shipping=False)
        if oder in Oder.objects():
            return {"message": "Đăth lằm đặt lốn!"}, 404
        oder.save()
        add_oder = Oder.objects().with_id(oder.id)
        #apikey = "AAAAhgLLpbs:APA91bGLuFvqDwvWs7L7RNnMHwus426M1fi5oLSP2azB5jOhB2jW2i91uIZF7jrECoyUYk-c-h5yyp4DY0oKFhEgg3S6o7fsv7dc-M5aBDdwxbYaWgXVn3HFEqImNYEm6xfyeMqb4lAR"
        #push_service = FCMNotification(api_key=apikey)
        #push_service.notify_topic_subscribers(topic_name="admin", message_body="Có đơn hàng mới",
        #                                      message_title="Kiểm tra ngay")
        return mlab.item2json(add_oder), 200


class OderSuccus(Resource):
    def put(self, id):
        oder = Oder.objects().with_id(id)
        if (oder.is_Succues == True):
            return {"message": "Cộng rồi"}, 401
        oder.update(set__is_Succues=True, set__is_Received=True, set__is_Shipping=True)
        oder_add = Oder.objects().with_id(id)
        user = oder["user"]
        spend = float(oder["spend"])
        spend_user = float(user["total_spend"])
        total = spend + spend_user
        user.update(total_spend=total)
        if user.token is not None:
            name = "bạn"
        if user.name is not None:
            name = user.name
            apikey = "AAAAhgLLpbs:APA91bGLuFvqDwvWs7L7RNnMHwus426M1fi5oLSP2azB5jOhB2jW2i91uIZF7jrECoyUYk-c-h5yyp4DY0oKFhEgg3S6o7fsv7dc-M5aBDdwxbYaWgXVn3HFEqImNYEm6xfyeMqb4lAR"
            push_service = FCMNotification(api_key=apikey)
            push_service.notify_single_device(registration_id=user.token, message_body="Chúc bạn ngon miệng!",
                                              message_title="Cảm ơn " + name + "!")
        return user.get_json(), 200

    def delete(self, id):
        oder = Oder.objects().with_id(id)
        oder.delete()
        user = oder.user
        if user.token is not None:
            apikey = "AAAAhgLLpbs:APA91bGLuFvqDwvWs7L7RNnMHwus426M1fi5oLSP2azB5jOhB2jW2i91uIZF7jrECoyUYk-c-h5yyp4DY0oKFhEgg3S6o7fsv7dc-M5aBDdwxbYaWgXVn3HFEqImNYEm6xfyeMqb4lAR"
            push_service = FCMNotification(api_key=apikey)
            push_service.notify_single_device(registration_id=user.token,
                                              message_body="Đơn hàng của bạn bị huỷ bỏ!",
                                              message_title="Cảm ơn bạn đã ghé thăm!")
        return {"message": "Ok"}, 200
    def patch(self,id):
        order=Oder.objects().with_id(id)
        order.update(set__is_Received=True)
        user = order.user
        if user.token is not None:
            apikey = "AAAAhgLLpbs:APA91bGLuFvqDwvWs7L7RNnMHwus426M1fi5oLSP2azB5jOhB2jW2i91uIZF7jrECoyUYk-c-h5yyp4DY0oKFhEgg3S6o7fsv7dc-M5aBDdwxbYaWgXVn3HFEqImNYEm6xfyeMqb4lAR"
            push_service = FCMNotification(api_key=apikey)
            push_service.notify_single_device(registration_id=user.token,
                                              message_body="Đơn hàng của bạn đã được tiếp nhận!",
                                              message_title="Tiếp nhận đơn hàng!")
        return {"message":"OK"},200

    def get(self, id):
        oder = Oder.objects().with_id(id)
        return oder.get_json()

class OrderShippingRes(Resource):
    def post(self,id):
        order = Oder.objects().with_id(id)
        order.update(set__is_Shipping=True,set__is_Received=True)
        user = order.user
        if user.token is not None:
            apikey = "AAAAhgLLpbs:APA91bGLuFvqDwvWs7L7RNnMHwus426M1fi5oLSP2azB5jOhB2jW2i91uIZF7jrECoyUYk-c-h5yyp4DY0oKFhEgg3S6o7fsv7dc-M5aBDdwxbYaWgXVn3HFEqImNYEm6xfyeMqb4lAR"
            push_service = FCMNotification(api_key=apikey)
            push_service.notify_single_device(registration_id=user.token,
                                              message_body="Đơn hàng đã được giao cho shipper!",
                                              message_title="Chú ý!")
        return {"message": "OK"}, 200


class OrderAdmin(Resource):
    def get(self):
        oders = Oder.objects(is_Succues=True)
        return [order.get_json() for order in oders], 200


class TotalMoneyDay(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="date", type=str, location="json")
        body = parser.parse_args()
        date = body["date"]
        orders = Oder.objects(date=date, is_Succues=True)
        print(len(orders))
        total_spend = 0
        for order in orders:
            total_spend += float(order.spend)

        return {"date": str(date),
                "total_spend": total_spend
                }

    def get(self):
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        orders = Oder.objects(date=date);
        total = 0;
        for item in orders:
            total += item.spend

        return {"total": total}


class TotalMoneyMonth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="month", type=str, location="json")
        body = parser.parse_args()
        month = body["month"]
        orders = Oder.objects(is_Succues=True)
        total_spend = 0
        for order in orders:
            if (str(order["date"]).find(str(month)) != -1):
                total_spend += order["spend"]

        return {"month": month,
                "total_spend": total_spend
                }

    def get(self):
        date = datetime.datetime.today().strftime('%m-%Y')
        print(date)
        orders = Oder.objects(is_Succues=True)
        total_spend = 0
        for order in orders:
            if (str(order["date"]).find(str(date)) != -1):
                total_spend += order["spend"]
        return {
            "total": total_spend
        }


class TotalMoneyYear(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="year", type=str, location="json")
        body = parser.parse_args()
        month = body["year"]
        a = int(month)
        if (len(month) != 4):
            return {"message": "gửi năm cl gì đấy"}, 401
        orders = Oder.objects(is_Succues=True)
        total_spend = 0
        for order in orders:
            if (str(order["date"]).find(str(month)) != -1):
                total_spend += order["spend"]

        return {"year": month,
                "total_spend": total_spend
                }


class TotalMoney(Resource):
    def get(self):
        orders = Oder.objects(is_Succues=True)
        total_spend = 0
        for order in orders:
            total_spend += float(order.spend)
        return {"Total": str(total_spend)}, 200
