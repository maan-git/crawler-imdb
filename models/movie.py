from configuration.mongodb_config import get_mongo_connection


class Movie:

    def __init__(self, id, title, year, summary, rating, stars, directors, genre):
        self.id = id
        self.title = title
        self.year = year
        self.summary = summary
        self.rating = rating
        self.stars = stars
        self.directors = directors
        self.genre = genre

    def to_dict(self):
        dict_res = {"id": self.id,
                    "title": self.title,
                    "summary": self.summary,
                    "year": self.year,
                    "rating": self.rating,
                    "stars": self.stars,
                    "directors": self.directors,
                    "genre": self.genre}
        return dict_res

    def save_movie(self):
        client_mongo = get_mongo_connection()
        db = client_mongo.movie
        movie_id = db.insert_one(self.to_dict()).inserted_id
        return movie_id

    def save_movies(self, movies):
        client_mongo = get_mongo_connection()
        db = client_mongo.movie
        result = db.insert_many(movies)
        return result.inserted_ids
