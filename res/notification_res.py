import datetime

from flask_restful import Resource, reqparse

from model.notification import *
from pyfcm.fcm import FCMNotification
import pytz


class PushNotification(Resource):
    def get(self):
        noti = Notification.objects()
        return [notif.get_json() for notif in noti]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="message_title", type=str, location="json")
        parser.add_argument(name="message_body", type=str, location="json")
        body = parser.parse_args()
        message_title = body["message_title"]
        message_body = body["message_body"]
        datet = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        if message_title is None or message_body is None:
            return {"message": "bắn noti cc thiếu"}, 401
        notification = Notification(message_body=message_body, message_title=message_title, datetime=str(datet),
                                    is_read=False)
        notification.save()
        listnoti = Notification.objects()
        if len(list(listnoti)) > 10:
            listnoti = list(listnoti)[:len(listnoti) - 11]
            for noti in listnoti:
                noti.delete()
        apikey = "AAAAhgLLpbs:APA91bGLuFvqDwvWs7L7RNnMHwus426M1fi5oLSP2azB5jOhB2jW2i91uIZF7jrECoyUYk-c-h5yyp4DY0oKFhEgg3S6o7fsv7dc-M5aBDdwxbYaWgXVn3HFEqImNYEm6xfyeMqb4lAR"
        push_service = FCMNotification(api_key=apikey)
        push_service.notify_topic_subscribers(topic_name="user", message_body=message_body,
                                              message_title=message_title)
        return mlab.item2json(Notification.objects().with_id(notification.id))


class ReadNoti(Resource):
    def put(self, id):
        noti = Notification.objects().with_id(id)
        noti.update(set__is_read=True)
        return {"message": "OK"}, 200
