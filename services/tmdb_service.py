from repositories import tmdb_repository, db_repository
from shared.models import TMDBPersonCredit


def get_actor_movie_credits(imdb_id):
    """
    Get a list of movie credits for a given actor
    :rtype: list of TMDBPersonCredit
    """
    tmdb_id = __get_tmdb_id(imdb_id)
    if tmdb_id is None:
        return None
    result = tmdb_repository.get_person_movie_credits(tmdb_id)
    if result is None:
        return None
    credit_list = []
    for movie in result['cast']:
        credit_list.append(TMDBPersonCredit.from_tmdb_person_credits_response_item(movie))
    return credit_list


def get_imdb_id(movie_tmdb_id):
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
