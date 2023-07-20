import requests
import redis
from functools import wraps

# Connect to the Redis server
r = redis.Redis()

def url_access_count(method):
    """Decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        access_count_key = f"count:{url}"
        access_count = r.get(access_count_key)
        if not access_count:
            access_count = 0
        else:
            access_count = int(access_count.decode('utf-8'))

        # Increment the access count and store it in Redis
        access_count += 1
        r.set(access_count_key, access_count)

        # Check if the URL is already cached in Redis
        cached_key = f"cached:{url}"
        html_content = r.get(cached_key)
        if html_content:
            return html_content.decode('utf-8')

        # Get new content and update cache
        html_content = method(url)

        r.setex(cached_key, 10, html_content)
        return html_content

    return wrapper

@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return ""

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    get_page(url)

