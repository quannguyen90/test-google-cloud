# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START gae_python38_datastore_store_and_fetch_times]
from google.cloud import datastore
from flask import request
from flask import Flask
import json
from flask import jsonify
from flask_pymongo import PyMongo
import random
import string

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/api/order/create', methods = ["POST"])
def order_create():
    req_data = request.get_json()
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=4))
    req_data["order_code"] = res
    collist = mongo.db.list_collection_names()
    order_collection = mongo.db["order"]
    if "order" in collist:
        print("The collection exists.")
    else:
        order_collection = mongo.db["order"]

    x = order_collection.insert_one(req_data)
    req_data["_id"] = str(x.inserted_id)
    return {"data": req_data}

@app.route('/api/order/list')
def order_list():
    collist = mongo.db.list_collection_names()
    if "order" in collist:
        collection = mongo.db["order"]
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
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=4))
    req_data["expense_code"] = res
    collist = mongo.db.list_collection_names()
    order_collection = mongo.db["expense"]
    if "expense" in collist:
        print("The collection exists.")
    else:
        order_collection = mongo.db["expense"]

    x = order_collection.insert_one(req_data)
    req_data["_id"] = str(x.inserted_id)
    return {"data": req_data}

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
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
