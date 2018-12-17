import re
from bs4 import BeautifulSoup

from models.movie import Movie
from services.imdb_service import get_webpage_service


def imdb_crawl(limit=10, min_rating=5):
    movies_indexed_so_far = 0
    genres = (
        "action", "comedy", "mystery", "sci_fi", "adventure", "fantasy", "horror", "animation", "drama", "thriller")
    iteration = 0
    count = 0
    while count < limit:
        for genre in genres:
            if count > limit:
                break
            c = get_webpage_service(genre, iteration)
            if c == None:
                continue
            soup = BeautifulSoup(c.data)
            data = _make_movie_object(soup, min_rating)
            count += 50
        iteration += 1

    return data


def save_movies(movies):
    movie = Movie()
    movie.save_movies(movies)


def _make_movie_object(soup, min_rating):
    data = []
    div_movies = soup.findAll("div", {"class": "lister-item mode-advanced"})
    for div_movie in div_movies:
        name = get_movie_name(div_movie)
        year = get_movie_year(div_movie)
        movie_id = get_movie_id(div_movie)
        rating = get_movie_rating(div_movie)
        stars = get_movie_stars(div_movie)
        directors = get_movie_directors(div_movie)
        summary = get_movie_summary(div_movie)
        genre = get_movie_genre(div_movie)

        movie = Movie(id=movie_id, title=name, summary=summary, year=year,
                      rating=rating, stars=stars, directors=directors, genre=genre)

        try:
            movie.save_movie()
        except Exception as ex:
            print("Error during saving movie ", movie.id)
            print("Error: ", ex)

        data.append(movie.to_dict())
    return data


def get_movie_name(div_movie):
    try:
        text = div_movie.find("h3", {"class": "lister-item-header"}).text
        text = text.replace('\n', ' ')
        extract = re.search('\d+\.[ ^\S\n\t](.*)[ ^\S\n\t]\(\d+\)', text.replace('\n', ' '))
        res = extract.group(1)
        return res

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the title of this movie")


def get_movie_rating(div_movie):
    div = div_movie.find("div", {"inline-block ratings-imdb-rating"})
    if div:
        return div.strong.text
    else:
        return 0


def get_movie_stars(div_movie):
    try:
        text = div_movie.find_all("p", {"class": ""})[1].text
        text = text.replace('\n', ' ')
        extract = re.search('Stars:\s(.*)', text)
        res = extract.group(1)
        res = res.split(",")
        return res

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the stars of this movie")


def get_movie_directors(div_movie):
    try:
        text = div_movie.find_all("p", {"class": ""})[1].text
        text = text.replace('\n', ' ')
        extract = re.search('(.*)Director:\s(.*)[\|\*]|(.*)Directors:\s(.*)[\|\*]', text)
        if "Directors" in text:
            res = extract.group(4)
        else:
            res = extract.group(2)

        res = res.split(",")
        return res

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the directors of this movie")


def get_movie_year(div_movie):
    if div_movie.find("h3", {"class": "lister-item-header"}):
        _ = div_movie.find("h3", {"class": "lister-item-header"}).text
        try:
            extract = re.search(r'(?!0000)\d{4}', _)
            extract = extract.group()
            return extract
        except Exception as ex:
            print("Error: ", ex)
            print("Error getting the year of this movie")
    else:
        raise ("Error getting the year of this movie")


def get_movie_id(div_movie):
    try:
        text = div_movie.find("h3", {"class": "lister-item-header"}).text
        extract = re.search('\d+', text)
        res = extract.group()
        return res

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the id of this movie")


def get_movie_genre(div_movie):
    try:
        text = div_movie.find("span", {"class": "genre"}).text
        text = text.replace('\n', '').replace(' ', '')
        text = text.split(",")
        return text

    except Exception as ex:
        print("Error: ", ex)
        print("Error getting the genre of this movie")


def get_movie_summary(div_movie):
    text = div_movie.find_all("p", {"class": "text-muted"})[1].text
    text = text.replace('\n', ' ')
    return text
