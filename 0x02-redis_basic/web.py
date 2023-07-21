#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching."""


import requests
import redis

# Create a redis client
r = redis.Redis()

# Define a decorator function for caching
def cache(func):
    """A decorator function that caches the result of another function.

    Args:
        func (function): The function to be cached.

    Returns:
        function: A wrapper function that checks the cache before calling the original function.
    """
    def wrapper(url: str) -> str:
        """A wrapper function that checks the cache before calling the original function.

        Args:
            url (str): The URL to be fetched.

        Returns:
            str: The HTML content of the URL.
        """
        # Check if the url is already cached
        cached = r.get(url)
        if cached:
            # Increment the count for the url
            r.incr(f"count:{url}")
            # Return the cached content
            return cached.decode()
        else:
            # Call the original function
            content = func(url)
            # Cache the content with an expiration time of 10 seconds
            r.setex(url, 10, content)
            # Set the count for the url to 1
            r.set(f"count:{url}", 1)
            # Return the content
            return content
    return wrapper

# Define a function to get the HTML content of a URL using requests
@cache # Apply the cache decorator
def get_page(url: str) -> str:
    """A function to get the HTML content of a URL using requests.

    Args:
        url (str): The URL to be fetched.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

# Test the function with a slow URL
url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
get_page(url)

