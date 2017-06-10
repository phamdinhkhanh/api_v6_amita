import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds119302.mlab.com:19302/order
host = "ds119302.mlab.com"
port = 19302
db_name = "order"
username = "khanh"
password = "khanh"



def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)


def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())