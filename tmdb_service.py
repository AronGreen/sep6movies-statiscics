import db_repository
import tmdb_repository
from models import TMDBPersonCredit

#
# __api_key = 'api_key=ec7d92089b9c745af52acceedbfe66fc'
# __base_url = 'https://api.themoviedb.org/3/'


def get_actor_movies(imdb_id):
    tmdb_id = __get_tmdb_id(imdb_id)
    if tmdb_id is None:
        return None
    result = tmdb_repository.get_person_movie_credits(tmdb_id)
    credit_list = []
    for movie in result['cast']:
        credit_list.append(TMDBPersonCredit.from_tmdb_person_credits_response_item(movie))
    return credit_list


def find(imdb_id):
    """
    Find the movie or person that matches the provided imdb id or None.
    :param imdb_id: imdb id of object
    :return: object that matches the imdb id can be a movie or person or None
    """
    return tmdb_repository.find(imdb_id)


def get_get_imdb_id(movie_tmdb_id):
    return db_repository.get_imdb_id(movie_tmdb_id) or \
           __get_imdb_id(movie_tmdb_id)


def __get_imdb_id(tmdb_id):
    imdb_id = tmdb_repository.get_imdb_id(tmdb_id)
    if bool(imdb_id):
        db_repository.insert_id_map(imdb_id=imdb_id, tmdb_id=tmdb_id)
    return imdb_id


def __get_tmdb_id(imdb_id):
    return db_repository.get_tmdb_id(imdb_id) or \
           __get_tmdb_id_from_api(imdb_id)


def __get_tmdb_id_from_api(imdb_id):
    tmdb_id = tmdb_repository.get_tmdb_id(imdb_id)
    print(f'get id result: {tmdb_id}')
    if bool(tmdb_id):
        db_repository.insert_id_map(imdb_id=imdb_id, tmdb_id=tmdb_id)
    return tmdb_id
