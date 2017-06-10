from flask import Flask
import mlab
from flask_restful import Resource, Api
from res.food_res import *
from res.user_res import *
from res.oder_res import *
from res.notification_res import *
from res.comment_res import *
from res.gift_res import *

mlab.connect()

app = Flask(__name__)
api = Api(app)
api.add_resource(FoodRes,"/food")
api.add_resource(UserRegister,"/user")
api.add_resource(UserUpdate,"/user/<id>")
api.add_resource(OderRes, "/oder")
api.add_resource(OderSuccus,"/oder/<id>")
api.add_resource(FoodRate,"/rate/<id>")
api.add_resource(FoodGetHotSales,"/food/hot")
api.add_resource(FoodFavorite,"/food/favorite")
api.add_resource(UserFoodLike,"/food/like/<id>")
api.add_resource(OrderAdmin,"/oder/success")
api.add_resource(UserOrderVerify,"/oder/<id>/verify")
api.add_resource(UserOrderSuccess,"/oder/<id>/success")
api.add_resource(TotalMoneyDay,"/oder/moneyday")
api.add_resource(TotalMoneyMonth,"/oder/moneymonth")
api.add_resource(TotalMoneyYear,"/oder/moneyyear")
api.add_resource(TotalMoney,"/oder/money")
api.add_resource(PushNotification,"/notification")
api.add_resource(FoodLike,"/food/islike/<id>")
api.add_resource(CommentRes,"/comment/<id>")
api.add_resource(UserSpend,"/oder/totalspend/<id>")
api.add_resource(FoodInfoRes,"/food/info")
api.add_resource(FoodInfoGetRes,"/food/info/<id>")
api.add_resource(GetCover,"/cv")
api.add_resource(GiftRes,"/giftcode")
api.add_resource(OrderShippingRes,"/oder/ship/<id>")
api.add_resource(TokenRes, "/token/<id>")
api.add_resource(UserThanThiet, "/users/tt")
api.add_resource(UserRanking, "/rank/<id>")
api.add_resource(ReadNoti, "/notification/<id>")

if __name__ == '__main__':
    app.run()
