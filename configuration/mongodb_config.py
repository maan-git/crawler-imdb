from pymongo import MongoClient
from flask import g


def get_mongo_connection():
    if 'mongo_connection_client' not in g:
        init_mongo_connection_client()
    return g.mongo_connection_client


def init_mongo_connection_client():
    host = 'db'
    port = '27017'
    password = 'crawler_imdb'
    user = 'crawler_imdb'
    database = 'mdb_crawler_imdb'
    client = MongoClient("mongodb://" + user + ":" + password + "@" + host +
                         ":" + port + "/" + database)[database]
    g.mongo_connection_client = client
    return g.mongo_connection_client
