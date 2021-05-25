
class TMDBMovie(object):
    __slots__ = ('tmdb_id', 'imdb_id', 'title', 'released', 'budget', 'imdb_rating')

    def __init__(self, tmdb_id, imdb_id, title, released, budget):
        self.tmdb_id = tmdb_id
        self.imdb_id = imdb_id
        self.title = title
        self.released = released
        self.budget = budget
        self.imdb_rating = ""

    @staticmethod
    def from_tmdb_movie_response(resp):
        return TMDBMovie(
            tmdb_id=resp['id'],
            imdb_id=resp['imdb_id'],
            title=resp['title'],
            released=resp['release_date'],
            budget=resp['budget']
        )


class OMDBMovie(object):
    __slots__ = ('title', 'released', 'director', 'imdb_rating', 'imdb_id', 'box_office')

    def __init__(self, title, released, director, imdb_rating, imdb_id, box_office):
        self.title = title
        self.released =released
        self.director = director
        self.imdb_rating = imdb_rating
        self.imdb_id = imdb_id
        self.box_office = box_office

    @staticmethod
    def from_omdb_movie_response(resp):
        return OMDBMovie(
            title=resp['Title'],
            released=resp['Released'],
            director=resp['Director'],
            imdb_rating=resp['imdbRating'],
            imdb_id=resp['imdbID'],
            box_office=['BoxOffice']
        )


class TMDBMovieCredit(object):
    """
    Represents an person in the list of credits for a movie
    """
    __slots__ = ('name', 'person_tmdb_id', 'character')

    def __init__(self, name, person_tmdb_id, character):
        self.name = name
        self.person_tmdb_id = person_tmdb_id
        self.character = character

    @staticmethod
    def from_tmdb_movie_credits_response_item(resp):
        return TMDBMovieCredit(
            name=resp['name'],
            person_tmdb_id=resp['id'],
            character=resp['character']
        )


class TMDBPersonCredit(object):
    """
    Represents an entry in a persons work history - a movie they worked on
    """
    __slots__ = ('title', 'movie_tmdb_id', 'movie_imdb_id', 'character', 'released', 'imdb_rating')

    def __init__(self, title, movie_tmdb_id, character, released):
        self.title = title
        self.movie_tmdb_id = movie_tmdb_id
        self.character = character
        self.released = released

    @staticmethod
    def from_tmdb_person_credits_response_item(resp):
        return TMDBPersonCredit(
            title=resp.get('title'),
            movie_tmdb_id=resp.get('id'),
            character=resp.get('character'),
            released=resp.get('release_date')
        )
