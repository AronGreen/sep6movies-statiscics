from flask import Flask, Response

import omdb_service
import tmdb_service
import jsonpickle
import concurrent.futures
import settings

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/actor/<imdb_id>/movieratings')
def actor_movie_ratings(imdb_id):
    movies = tmdb_service.get_actor_movies(imdb_id)
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings.thread_pool_max_threads()) as executor:
        futures = [executor.submit(__map_imdb_info, movie) for movie in movies]
        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

    return __json_response(jsonpickle.encode({'movies': movies}, unpicklable=False))


def __map_imdb_info(m):
    m.movie_imdb_id = tmdb_service.get_get_imdb_id(m.movie_tmdb_id)
    m.imdb_rating = omdb_service.get_imdb_rating(m.movie_imdb_id)


def __json_response(jsn):
    return Response(jsn, mimetype='application/json')


if __name__ == '__main__':
    app.run()
