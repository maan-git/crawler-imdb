from bson import json_util, ObjectId
import json
from configuration.mongodb_config import get_mongo_connection


class Movie:

    def __init__(self, id: int, title: str, runtime: float, year: int, summary: str, rating: float, stars: int,
                 directors: list,
                 genre: list):
        self.id = id
        self.title = title
        self.runtime = runtime
        self.year = year
        self.summary = summary
        self.rating = rating
        self.stars = stars
        self.directors = directors
        self.genre = genre

    def to_dict(self):
        dict_res = {"id": self.id,
                    "title": self.title,
                    "runtime": self.runtime,
                    "summary": self.summary,
                    "year": self.year,
                    "rating": self.rating,
                    "stars": self.stars,
                    "directors": self.directors,
                    "genre": self.genre}
        return dict_res

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def save_movie(self):
        client = get_mongo_connection()
        db = client.get_database()
        movie_db = db['movie']
        movie_id = movie_db.insert_one(self.to_dict()).inserted_id

        return movie_id

    @staticmethod
    def save_movies(movies):
        client = get_mongo_connection()
        db = client.get_database()
        movie_db = db['movie']
        result = movie_db.insert_many(movies)
        return result

    @staticmethod
    def get_movies():
        client = get_mongo_connection()
        db = client.get_database()
        movie_db = db['movie']
        result = movie_db.find()
        return result
