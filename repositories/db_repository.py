from _datetime import datetime, timedelta
from shared import settings
import mysql.connector


def insert_id_map(imdb_id, tmdb_id):
    __execute_p(
        '''INSERT INTO id_map (imdb_id, tmdb_id) VALUES (%s, %s)''',
        (imdb_id, tmdb_id,)
    )


def insert_imdb_rating(imdb_id, rating):
    __execute_p(
        '''insert into imdb_ratings (imdb_id, imdb_rating) values (%s, %s)''',
        (imdb_id, rating,)
    )


def get_tmdb_id(imdb_id):
    """
    Try to get a tmdb id from the corresponding imdb id
    :rtype: str | None
    """
    result = __fetchone(
        '''SELECT tmdb_id FROM id_map WHERE imdb_id = %s ''',
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
        '''SELECT imdb_id FROM id_map WHERE tmdb_id = %s ''',
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
        '''SELECT imdb_rating, updated FROM imdb_ratings WHERE imdb_id = %s ''',
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
        '''delete from imdb_ratings where imdb_id = %s''',
        (imdb_id,)
    )


def __execute_p(sql, parameters=...):
    con = __get_con()
    cur = con.cursor()
    cur.execute(sql, parameters)
    con.commit()
    cur.close()
    con.close()


def __execute(sql):
    con = __get_con()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()


def __fetchone(sql, parameters=...):
    con = __get_con()
    cur = con.cursor()
    cur.execute(sql, parameters)
    result = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    return result


def __get_con():
    return mysql.connector.connect(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE
    )


def __init_db():
    __execute('''CREATE TABLE IF NOT EXISTS id_map
                   (imdb_id varchar(10),
                   tmdb_id varchar(10),
                   PRIMARY KEY (imdb_id, tmdb_id))
                   ''')
    __execute('''CREATE TABLE IF NOT EXISTS imdb_ratings
                      (imdb_id varchar(10),
                      imdb_rating varchar(10),
                      updated timestamp default current_timestamp,
                      PRIMARY KEY (imdb_id))
                      ''')


__init_db()
