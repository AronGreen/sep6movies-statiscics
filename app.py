import concurrent.futures
from flask import Flask, Response, request
import jsonpickle
from services import omdb_service, tmdb_service
from shared import settings

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/search/people')
def search_people():
    search_string = request.args.get('query')
    return __json_response(tmdb_service.search_people(search_string))


@app.route('/tmdb_id/<imdb_id>')
def get_tmdb_id(imdb_id):
    return __json_response(tmdb_service.get_tmdb_id(imdb_id))


@app.route('/imdb_id/<tmdb_id>')
def get_imdb_id(tmdb_id):
    return __json_response(tmdb_service.get_imdb_id(tmdb_id))


@app.route('/actor/<imdb_id>/movieratings')
def actor_movie_ratings(imdb_id):
    movie_credits = tmdb_service.get_actor_movie_credits(imdb_id)
    if movie_credits is None:
        return __json_response([])
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings.THREAD_POOL_MAX_THREADS) as executor:
        futures = [executor.submit(__map_movie_credit_imdb_info, movie) for movie in movie_credits]
        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

    return __json_response(movie_credits)


def __map_movie_credit_imdb_info(m):
    m.movie_imdb_id = tmdb_service.get_imdb_id(m.movie_tmdb_id)
    m.imdb_rating = omdb_service.get_imdb_rating(m.movie_imdb_id)


def __json_response(obj):
    return Response(jsonpickle.encode(obj, unpicklable=False), mimetype='application/json')


if __name__ == '__main__':
    app.run()
