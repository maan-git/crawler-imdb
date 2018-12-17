from flask import Flask


def create_app():
    my_app = Flask(__name__)
    my_app.debug = True
    my_app.config['JSON_SORT_KEYS'] = False

    with my_app.app_context():
        from configuration.imdb_client import (
            get_imdb_service
        )
        get_imdb_service()

        from configuration.mongodb_config import (
            get_mongo_connection
        )
        get_mongo_connection()

    return my_app


app = create_app()
