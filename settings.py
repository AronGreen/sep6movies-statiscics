import os
from dotenv import load_dotenv

load_dotenv()


def thread_pool_max_threads(): return int(os.environ['thread_pool_max_threads'])


def omdb_api_key(): return os.environ['omdb_api_key']


def tmdb_api_key(): return os.environ['tmdb_api_key']