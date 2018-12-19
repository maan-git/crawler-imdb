import urllib3
from flask import g


def get_imdb_service():
    """
    Gets PoolManager method from urllib3 and insert it in Flask global variable 'g'
    :return: PoolManager inserted in g variable
    """
    if 'soap_imdb_service_client' not in g:
        init_imdb_service()
    return g.soap_imdb_service_client


def init_imdb_service():
    client = urllib3.PoolManager()
    g.soap_imdb_service_client = client
    return g.soap_imdb_service_client
