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
    def get(self):
        prefix = 'go'
        limit = 5
        offset = 0
        all_documents = mycol_1.find({ "name": {'$regex': '/'+prefix+'/'}})
        for document in all_documents:
        	print(document)
        # return Response(str(all_rows))

class Movies(Resource):
    def get(self,movie_id):
        all_documents = mycol_1.find({'_id':movie_id})
        for document in all_documents:
            print(document)

api.add_resource(Autocomplete, '/autocomplete')
api.add_resource(Movies, '/movies/<movie_id>')

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
