import jsonpickle

str = """{"title": "American History X", "movie_tmdb_id": 73, "character": "Derek Vinyard", "released": "1998-10-30"}"""

res = jsonpickle.decode(str)

print(type(res))
