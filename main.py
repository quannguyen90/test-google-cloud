from flask import request
from flask import Flask
from flask import jsonify
from flask_pymongo import PyMongo
import random
import string
from datetime import datetime, date, time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/api/order/create', methods = ["POST"])
def order_create():
    req_data = request.get_json()
    print('request data:  ', req_data)
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=4))
    req_data["order_code"] = res
    req_data['created_at'] = datetime.timestamp(datetime.now())
    collist = mongo.db.list_collection_names()
    order_collection = mongo.db["order"]
    if "order" in collist:
        print("The collection exists.")
    else:
        order_collection = mongo.db["order"]

    x = order_collection.insert_one(req_data)
    req_data["_id"] = str(x.inserted_id)
    return {"data": req_data}

@app.route('/api/order/list_today')
def order_list_today():
    collist = mongo.db.list_collection_names()
    if "order" in collist:
        collection = mongo.db["order"]
        # now = datetime.now()
        start = datetime.combine(date.today(), time())
        end = datetime.combine(date.today(), time(23, 59))
        startTimestamp = datetime.timestamp(start)
        endTimestamp = datetime.timestamp(end)
        print('start', startTimestamp)
        print('end', endTimestamp)
        documents = collection.find({"created_at": {'$gt': startTimestamp, '$lt': endTimestamp}})
        response = []
        for document in documents:
            document['_id'] = str(document['_id'])
            response.append(document)
        return jsonify({
            "data": response
        })
    return {
        "data": []
    }

@app.route('/api/order/list')
def order_list():
    collist = mongo.db.list_collection_names()
    if "order" in collist:
        collection = mongo.db["order"]
        # now = datetime.now()
        documents = collection.find()
        response = []
        for document in documents:
            document['_id'] = str(document['_id'])
            response.append(document)
        return jsonify({
            "data": response
        })
    return {
        "data": []
    }

@app.route('/api/expense/create', methods = ["POST"])
def expense_create():
    req_data = request.get_json()
    print('request data:  ', req_data)
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=4))
    req_data["expense_code"] = res
    req_data['created_at'] = datetime.timestamp(datetime.now())
    collist = mongo.db.list_collection_names()
    order_collection = mongo.db["expense"]
    if "expense" in collist:
        print("The collection exists.")
    else:
        order_collection = mongo.db["expense"]

    x = order_collection.insert_one(req_data)
    req_data["_id"] = str(x.inserted_id)
    return {"data": req_data}

@app.route('/api/expense/list_today')
def expense_list_today():
    collist = mongo.db.list_collection_names()
    if "expense" in collist:
        collection = mongo.db["expense"]
        start = datetime.combine(date.today(), time())
        end = datetime.combine(date.today(), time(23, 59))
        startTimestamp = datetime.timestamp(start)
        endTimestamp = datetime.timestamp(end)
        print('start', startTimestamp)
        print('end', endTimestamp)
        documents = collection.find({"created_at": {'$gt': startTimestamp, '$lt': endTimestamp}})
        response = []
        for document in documents:
            document['_id'] = str(document['_id'])
            response.append(document)
        return jsonify({
            "data": response
        })
    return {
        "data": []
    }

@app.route('/api/expense/list')
def expense_list():
    collist = mongo.db.list_collection_names()
    if "expense" in collist:
        collection = mongo.db["expense"]
        documents = collection.find()
        response = []
        for document in documents:
            document['_id'] = str(document['_id'])
            response.append(document)
        return jsonify({
            "data": response
        })
    return {
        "data": []
    }

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
    # app.run(host='192.168.1.3')
# --host=192.168.1.3 --port=5000