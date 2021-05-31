import os
from dotenv import load_dotenv

load_dotenv()

THREAD_POOL_MAX_THREADS = int(os.environ['thread_pool_max_threads'])
OMDB_API_KEY = os.environ['omdb_api_key']
TMDB_API_KEY = os.environ['tmdb_api_key']
MYSQL_HOST = os.environ['mysql_host']
MYSQL_USER = os.environ['mysql_user']
MYSQL_PASSWORD = os.environ['mysql_password']
MYSQL_DATABASE = os.environ['mysql_database']