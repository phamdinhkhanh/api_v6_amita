from flask_restful import Resource, reqparse
from model.oder import *
from model.user import User
from model.food import Food
import mlab
from pyfcm.fcm import FCMNotification
import json
import requests
from model.comment import *
import datetime


class CommentRes(Resource):
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id_user", type=str, location="json")
        parser.add_argument(name="message", type=str, location="json")
        body = parser.parse_args()
        id_user = body["id_user"]
        message = body["message"]
        print(id_user)
        print(message)
        food = Food.objects().with_id(id)
        user=User.objects().with_id(id_user)
        date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        comment=Comment(user=user,message=message,date=str(date),food=food)
        comment.save()
        comment_add=Comment.objects().with_id(comment.id)
        return comment_add.get_json(),200
    def get(self,id):
        food=Food.objects().with_id(id)
        comments=Comment.objects(food=food)
        return [comment.get_json() for comment in comments],200
