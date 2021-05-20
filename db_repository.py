import sqlite3
from _datetime import datetime, timedelta


def insert_id_map(imdb_id, tmdb_id):
    __execute_p(
        '''INSERT INTO id_map (imdb_id, tmdb_id) VALUES (?, ?)''',
        (imdb_id, tmdb_id,)
    )


def insert_imdb_rating(imdb_id, rating):
    __execute_p(
        '''insert into imdb_ratings (imdb_id, imdb_rating) values (?, ?)''',
        (imdb_id, rating,)
    )


def get_tmdb_id(imdb_id):
    """
    Try to get a tmdb id from the corresponding imdb id
    :rtype: str | None
    """
    result = __fetchone(
        '''SELECT tmdb_id FROM id_map WHERE imdb_id = ? ''',
        (imdb_id,)
    )
    if result is None:
        return None
    return result[0]


def get_imdb_id(tmdb_id):
    """
    Try to get a imdb id from the corresponding tmdb id
    :rtype: str | None
    """
    result = __fetchone(
        '''SELECT imdb_id FROM id_map WHERE tmdb_id = ? ''',
        (tmdb_id,)
    )
    if result is None:
        return None
    return result[0]


def get_imdb_rating(imdb_id):
    """
    Try to get an imdb rating for a movie.
    If the stored rating is older than 7 days,
    it will be deleted and None returned.
    :rtype: str | None
    """
    result = __fetchone(
        '''SELECT imdb_rating, updated FROM imdb_ratings WHERE imdb_id = ? ''',
        (imdb_id,)
    )
    if result is None:
        return None
    if datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S') < (datetime.now() - timedelta(days=7)):
        __delete_imdb_rating(imdb_id)
        return None
    return result[0]


def __delete_imdb_rating(imdb_id):
    __execute_p(
        '''delete from imdb_ratings where imdb_id = ?''',
        (imdb_id,)
    )


def __execute_p(sql, parameters=...):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cur.execute(sql, parameters)
    con.commit()
    cur.close()


def __execute(sql):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()


def __fetchone(sql, parameters=...):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    cur.execute(sql, parameters)
    result = cur.fetchone()
    cur.close()
    return result


def __init_db():
    __execute('''CREATE TABLE IF NOT EXISTS id_map
                   (imdb_id text,
                   tmdb_id text,
                   PRIMARY KEY (imdb_id, tmdb_id))
                   ''')
    __execute('''CREATE TABLE IF NOT EXISTS imdb_ratings
                      (imdb_id text,
                      imdb_rating text,
                      updated default current_timestamp,
                      PRIMARY KEY (imdb_id))
                      ''')


__init_db()
