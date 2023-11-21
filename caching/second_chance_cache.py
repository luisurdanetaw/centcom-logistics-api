import asyncio
from collections import deque
from datetime import datetime


def create_second_chance_cache(max_size=3):
    cache = {}
    lock = asyncio.Lock()

    async def get(page_reference):
        nonlocal cache
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with lock:
            print(f"{current_time} - Lock acquired for GET operation on page {page_reference}.")
            if page_reference in cache:
                # Mark the page as referenced (if it exists in the cache)
                print(f"{current_time} - Cache hit for page {page_reference}.")
                return cache[page_reference][0]
            else:
                # Page fault, return None for the data
                print(f"{current_time} - Cache miss for page {page_reference}.")
                return None

    async def put(page_reference, data):
        nonlocal cache
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with lock:
            print(f"{current_time} - Lock acquired for PUT operation on page {page_reference}.")
            if len(cache) < max_size:
                # Cache is not full, add the page
                cache[page_reference] = [data, True]
                print(f"{current_time} - Page {page_reference} added to the cache.")
            else:
                # Cache is full, apply Second Chance algorithm
                keys = deque(cache.keys())
                while True:
                    oldest_page = keys.popleft()
                    if not cache[oldest_page][1]:
                        # If not referenced, replace the page
                        cache.pop(oldest_page)
                        cache[page_reference] = [data, True]
                        print(f"{current_time} - Page {page_reference} added to the cache, replacing {oldest_page}.")
                        break
                    else:
                        # Mark the page as not referenced
                        cache[oldest_page][1] = False
                        keys.append(oldest_page)
                        print(f"{current_time} - Page {oldest_page} marked as not referenced.")

    async def print_cache():
        nonlocal cache
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Current cache state: {cache}")

    return get, put, print_cache


