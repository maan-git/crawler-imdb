import pytest
import mock
import json
from bson import json_util, ObjectId
from mock import patch

from controller.controller import (imdb_crawl, _imdb_crawler, _save_movies, _get_movie_summary, _get_movie_runtime,
                                   _get_movie_genre)
from tests.base import TestCase


class TestController(TestCase):

    def test_imdb_crawl_limit_min_rating_values_success(self):
        with pytest.raises(ValueError):
            limit = 10
            min_rating = 5
            _imdb_crawler(limit=limit, min_rating=min_rating)

    def test_get_movie_summary_success(self):
        movie_summary = _get_movie_summary(div_movie="my_div_movie")

    def test_get_movie_summary_error(self):
        movie_summary = _get_movie_summary(div_movie="my_div_movie")
        assert movie_summary != str

    def test_get_movie_runtime_error(self):
        movie_runtime = _get_movie_runtime(div_movie="my_div_movie")
        assert movie_runtime != float

    def test_get_movie_runtime_success(self):
        movie_runtime = _get_movie_runtime(div_movie="my_div_movie")

    def test_get_movie_genre_success(self):
        movie_genre = _get_movie_genre(div_movie="my_div_movie")

    def test_get_movie_genre_error(self):
        movie_genre = _get_movie_genre(div_movie="my_div_movie")

        # movies = _imdb_crawler(limit=limit,min_rating=min_rating)
        # _save_movies(movies=movies)
        # movies = json.loads(json_util.dumps(movies))
        # assert type(movies) == list

