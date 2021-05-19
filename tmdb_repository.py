
import jsonpickle
import requests

__api_key = 'api_key=ec7d92089b9c745af52acceedbfe66fc'
__base_url = 'https://api.themoviedb.org/3/'


def find(imdb_id):
    """
    Find the movie or person that matches the provided imdb id or None.
    TMDb reference: https://developers.themoviedb.org/3/find/find-by-id
    :param imdb_id: imdb id of object
    :return: dict that matches the imdb id can be a movie or person or None
    """
    print(f'find {imdb_id}')
    url = f'{__base_url}/find/{imdb_id}?{__api_key}&external_source=imdb_id'
    resp = jsonpickle.decode(requests.request('GET', url).text)
    if bool(resp['movie_results']):
        return resp['movie_results'][0]
    if bool(resp['person_results']):
        return resp['person_results'][0]
    return None


def get_person_movie_credits(tmdb_id):
    """
    Get a dict with all movie credits for a person.
    Note that this includes both cast and crew credits.
    :param tmdb_id: person tmdb_id
    :return: dict of movie credits
    """
    print(f'get_person_movie_credits {tmdb_id}')
    url = f'{__base_url}/person/{tmdb_id}/movie_credits?{__api_key}&language=en-US'
    return jsonpickle.decode(requests.request('GET', url).text)


def get_tmdb_id(imdb_id):
    api_result = find(imdb_id)
    return api_result.get('id')


def get_imdb_id(tmdb_id):
    # afaik there is no way to know id a tmdb id is a movie or a person,
    # so working on an assumption that movies are requested more than
    # people, we check for movies first, then people if no movie was found
    result = __get_imdb_id_from_movie(tmdb_id)
    if result is None:
        result = __get_imdb_id_from_person(tmdb_id)
    return result or '-1'


def __get_imdb_id_from_movie(tmdb_id):
    print(f'__get_imdb_id_from_movie {tmdb_id}')
    url = f'{__base_url}/movie/{tmdb_id}/external_ids?{__api_key}'
    result = jsonpickle.decode(requests.request('GET', url).text)
    return result.get('imdb_id')


def __get_imdb_id_from_person(tmdb_id):
    print(f'__get_imdb_id_from_person {tmdb_id}')
    url = f'{__base_url}/person/{tmdb_id}/external_ids?{__api_key}'
    result = jsonpickle.decode(requests.request('GET', url).text)
    return result.get('imdb_id')

