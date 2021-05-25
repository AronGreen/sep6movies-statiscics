import jsonpickle
import requests
from shared import settings

__api_key = f'apikey={settings.OMDB_API_KEY}'
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
