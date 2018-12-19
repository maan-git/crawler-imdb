import pytest
import mock
import json
from bson import json_util, ObjectId
from mock import patch

from controller.controller import (imdb_crawl, _imdb_crawler, _save_movies)
from tests.base import TestCase

class TestController(TestCase):

    def test_imdb_crawl_limit_min_rating_values_success(self):
        with pytest.raises(ValueError):
            limit = 10
            min_rating = 5
            _imdb_crawler(limit=limit, min_rating=min_rating)

        #
        # movies = _imdb_crawler(limit=limit,min_rating=min_rating)
        # _save_movies(movies=movies)
        # movies = json.loads(json_util.dumps(movies))
        # assert type(movies) == list
