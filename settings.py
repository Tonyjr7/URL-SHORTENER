from pathlib import Path

from decouple import config

# This to build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

# Application's config values
URI_STRING : str = config("uri_string")