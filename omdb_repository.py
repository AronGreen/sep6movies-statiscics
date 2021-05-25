import jsonpickle
import requests
import settings


__api_key = f'apikey={settings.omdb_api_key()}'
__base_url = 'https://www.omdbapi.com/'


# def get_imdb_rating(imdb_id):
#     movie = get_movie(imdb_id)
#     if movie is None:
#         return None
#     return movie.get('imdbRating')


def get_movie(imdb_id):
    url = f'{__base_url}?i={imdb_id}&{__api_key}'
    result = jsonpickle.decode(requests.request('GET', url).text)
    if 'Error' in result:
        return None
    return result
