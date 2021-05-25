import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB_NAME = os.environ['sqlite_db_name']
THREAD_POOL_MAX_THREADS = int(os.environ['thread_pool_max_threads'])
OMDB_API_KEY = os.environ['omdb_api_key']
TMDB_API_KEY = os.environ['tmdb_api_key']
