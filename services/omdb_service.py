from repositories import omdb_repository, db_repository


def get_imdb_rating(imdb_id):
    rating = db_repository.get_imdb_rating(imdb_id)
    if rating is None:
        rating = __get_imdb_rating_from_api(imdb_id)
    return rating


def __get_imdb_rating_from_api(imdb_id):
    movie = omdb_repository.get_movie(imdb_id)
    db_repository.insert_imdb_rating(imdb_id, movie.get('imdbRating', '-1'))
    if movie is not None:
        return movie.get('imdbRating')
    return '-1'
