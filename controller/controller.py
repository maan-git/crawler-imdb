import re
import json
from bson import json_util, ObjectId
from bs4 import BeautifulSoup

from models.movie import Movie
from services.imdb_service import get_webpage_service

from excepts.service_errors import (
    CrawlerHttpError
)

def get_movies_imdb():
    try:
        movies = Movie.get_movies()
        movies = json.loads(json_util.dumps(movies))

        return movies

    except CrawlerHttpError as ex:
        raise ("Error during getting the movies: ", ex)


def imdb_crawl(limit: int = 50, min_rating: int = 0):
    try:
        movies = _imdb_crawler(limit=limit, min_rating=min_rating)
        _save_movies(movies=movies)
        movies = json.loads(json_util.dumps(movies))

        return movies

    except CrawlerHttpError as ex:
        raise ("Error during crawling: ", ex)


def _imdb_crawler(limit: int, min_rating: int):

    # print('Limit: ', limit)
    # genres = (
    #     "action", "comedy", "mystery", "sci_fi", "adventure", "fantasy", "horror", "animation", "drama", "thriller")
    genres = (
        "action", "comedy", "horror", "animation", "drama")
    iteration = 0
    count = 0
    data_movies = []
    while count < limit:
        for genre in genres:
            if count > limit:
                break
            c = get_webpage_service(genre, iteration)
            if c == None:
                continue
            soup = BeautifulSoup(c.data)
            data_movies = data_movies + _make_movie_object(soup, min_rating)
            count += 50
        iteration += 1

    return data_movies


def _make_movie_object(soup, min_rating=None):
    data = []
    div_movies = soup.findAll("div", {"class": "lister-item mode-advanced"})
    for div_movie in div_movies:
        #'bs4.element.Tag'
        print(type(div_movie))

        name = _get_movie_name(div_movie)
        year = _get_movie_year(div_movie)
        movie_id = _get_movie_id(div_movie)
        movie_runtime = _get_movie_runtime(div_movie)
        rating = _get_movie_rating(div_movie)
        stars = _get_movie_stars(div_movie)
        directors = _get_movie_directors(div_movie)
        summary = _get_movie_summary(div_movie)
        genre = _get_movie_genre(div_movie)

        movie = Movie(id=movie_id, title=name, runtime=movie_runtime, summary=summary, year=year,
                      rating=rating, stars=stars, directors=directors, genre=genre)

        data.append(movie.to_dict())

    return data


def _save_movie(movie):
    try:
        movie.save_movie()
    except Exception as ex:
        print("Error during saving movie ", movie.id)
        print("Error: ", ex)


def _save_movies(movies):
    try:
        Movie.save_movies(movies)
    except Exception as ex:
        print("Error during saving movie ", ex)


def _get_movie_name(div_movie):
    try:
        text = div_movie.find("h3", {"class": "lister-item-header"}).text
        text = text.replace('\n', ' ')
        extract = re.search('\d+\.[ ^\S\n\t](.*)[ ^\S\n\t]\(\d+\)', text.replace('\n', ' '))
        res = extract.group(1)
        return str(res)

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the title of this movie")


def _get_movie_rating(div_movie):
    div = div_movie.find("div", {"inline-block ratings-imdb-rating"})
    if div:
        return float(div.strong.text)
    else:
        return 0


def _get_movie_stars(div_movie):
    try:
        text = div_movie.find_all("p", {"class": ""})[1].text
        text = text.replace('\n', ' ')
        extract = re.search('Stars:\s(.*)', text)
        res = extract.group(1)
        res = res.split(",")
        res = [x.strip() for x in res]
        return res

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the stars of this movie")


def _get_movie_directors(div_movie):
    try:
        text = div_movie.find_all("p", {"class": ""})[1].text
        text = text.replace('\n', ' ')
        extract = re.search('(.*)Director:\s(.*)[\|\*]|(.*)Directors:\s(.*)[\|\*]', text)
        if "Directors" in text:
            res = extract.group(4)
        else:
            res = extract.group(2)

        res = res.split(",")
        res = [x.strip() for x in res]
        return res

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the directors of this movie")


def _get_movie_year(div_movie):
    if div_movie.find("h3", {"class": "lister-item-header"}):
        _ = div_movie.find("h3", {"class": "lister-item-header"}).text
        try:
            extract = re.search(r'(?!0000)\d{4}', _)
            extract = extract.group()
            return int(extract)
        except Exception as ex:
            print("Error: ", ex)
            print("Error getting the year of this movie")
    else:
        print("Error getting the year of this movie")


def _get_movie_id(div_movie):
    try:
        text = div_movie.find("h3", {"class": "lister-item-header"}).text
        extract = re.search('\d+', text)
        res = extract.group()
        return int(res)

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the id of this movie")


def _get_movie_genre(div_movie):
    try:
        text = div_movie.find("span", {"class": "genre"}).text
        text = text.replace('\n', '').replace(' ', '')
        text = text.split(",")
        return text

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the genre of this movie")


def _get_movie_runtime(div_movie):
    try:
        text = div_movie.find("span", {"class": "runtime"}).text
        text = text.split("min")
        return float(text[0].replace(' ', ''))

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the runtime of this movie")
        return 0.0


def _get_movie_summary(div_movie):
    text = div_movie.find_all("p", {"class": "text-muted"})[1].text
    text = text.replace('\n', ' ').strip()
    return text
