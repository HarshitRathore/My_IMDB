from flask import Flask, render_template, redirect, request, Response
import pymongo
from flask_restful import Resource, Api
import json
from flask_pymongo import PyMongo
# import gridfs
# import re

app = Flask(__name__)
api = Api(app)

dbname = "imdb"
colname_1 = "movies"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[dbname]
mycol_1 = mydb[colname_1]

# fs = gridfs.GridFS(mydb)

class Autocomplete(Resource):
    def get(self,params):
        prefix, limit, offset = params.split('_')
        limit = int(limit)
        offset = int(offset)
        sorted_list = []
        all_documents = mycol_1.find({})
        for document in all_documents:
            if document['name'].lower().startswith(prefix.lower()):
                sorted_list.append(document)
        for i in range(len(sorted_list)):
            for j in range(i,len(sorted_list)):
                if sorted_list[i]['rating'] > sorted_list[j]['rating']:
                    sorted_list[i],sorted_list[j] = sorted_list[j],sorted_list[i]
        try:
            # print(prefix,str(sorted_list[-1:-6:-1]))
            resp = Response(str(json.dumps(sorted_list[-1:-6:-1])),mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except Exception:
            # print(prefix,str(sorted_list))
            resp = Response(str(json.dumps(sorted_list)),mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

class Movies(Resource):
    def get(self,movie_id):
        sorted_list = []
        all_documents = mycol_1.find({'_id':movie_id})
        for document in all_documents:
            sorted_list.append(document)
        resp = Response(str(json.dumps(sorted_list)),mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

api.add_resource(Autocomplete, '/autocomplete/<params>')
api.add_resource(Movies, '/movies/<movie_id>')

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
