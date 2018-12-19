from flask import request, jsonify

from app import app

from controller.controller import (
    imdb_crawl, get_movies_imdb)


@app.route('/hello', methods=['POST'])
def hello():
    """
    Hello world endpoint for test
    :return: message hello
    """

    return jsonify({'message': 'Hello there!'})


@app.route('/crawl', methods=['POST'])
def crawl():
    """
    Crawl endpoint to crawler the data from imdb.com website
    :return: the data crawled
    """
    limit = request.get_json().get('limit', '')
    min_rate = request.get_json().get('min_rate', '')

    res = imdb_crawl(limit=limit, min_rating=min_rate)

    return jsonify(res)


@app.route('/get_movies', methods=['GET'])
def get_movies():
    """
    Crawl endpoint to crawler the data from imdb.com website
    :return: the data crawled
    """
    res = get_movies_imdb()

    return jsonify(res)

