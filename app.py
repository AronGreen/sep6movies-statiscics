from flask import Flask, Response

import omdb_service
import tmdb_service
import jsonpickle

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/actor/<imdb_id>/movieratings')
def actor_movie_ratings(imdb_id):
    result = {'movies': tmdb_service.get_actor_movies(imdb_id)}
    for movie in result['movies']:
        movie_imdb_id = tmdb_service.get_get_imdb_id(movie.movie_tmdb_id)
        movie.imdb_rating = omdb_service.get_imdb_rating(movie_imdb_id)
    return __json_response(jsonpickle.encode(result, unpicklable=False))


def __json_response(jsn):
    return Response(jsn, mimetype='application/json')


if __name__ == '__main__':
    app.run()
