from pymongo import MongoClient
from flask import g


def get_mongo_connection():
    """
    Gets MongoDB connection and insert it in Flask global variable 'g'
    :return: mongo_client_connection inserted in g variable
    """
    if 'mongo_connection_client' not in g:
        init_mongo_connection_client()

    return g.mongo_connection_client


def init_mongo_connection_client():
    password = 'crawler_2018_imdb'
    user = 'user_crawler_imdb'
    database = 'imdb_crawler'
    url = "mongodb://" + user + ":" + password + "@ds157818.mlab.com:57818/" + database
    client = MongoClient(url)
    g.mongo_connection_client = client

    return g.mongo_connection_client
