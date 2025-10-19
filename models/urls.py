from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from settings import URI_STRING

uri = URI_STRING

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["url_shortener"]
urls = db["urls"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("DB is accessible")
except Exception as e:
    print(e)

def add_url(original_url: str, short_code: str):
    """Add a new URL mapping to the database."""
    url_data = {
        "original_url": original_url,
        "short_code": short_code
    }

    # Insert the URL data into the collection
    urls.insert_one(url_data)

    # Return the short code
    return url_data["short_code"]

def get_original_url(short_code: str):
    """Retrieve the original URL from the database using the short code."""
    url_data = urls.find_one({"short_code": short_code})
    if url_data:
        return url_data["original_url"]
    return None