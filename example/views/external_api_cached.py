import time
import requests
from django.shortcuts import render
from django.core.cache import cache


EXTERNAL_API_MOCK_URL = "https://jsonplaceholder.typicode.com/posts/1"


def get_external_api_data(item_id, enable_cache=True):
    """Simulates a slow external API call."""
    cache_key = f'external_api_data_{item_id}'
    data = cache.get(cache_key) if enable_cache else None

    if data is None:
        print(f"--- Getting external API data for {item_id} (no cache) ---")
        try:
            # Simulate real network latency
            start_time = time.time()
            response = requests.get(f'{EXTERNAL_API_MOCK_URL}')
            end_time = time.time()
            print(
                f"   External API latency: {end_time - start_time:.2f} seconds")

            response.raise_for_status()
            data = response.json()
            if enable_cache:
                cache.set(cache_key, data, timeout=60 * 60)
        except requests.exceptions.RequestException as e:
            print(f"Error getting external API data: {e}")
            data = {"error": "Could not retrieve external data."}
    else:
        print(f"--- Getting external API data for {item_id} (from cache) ---")
    return data


def external_api_cached_view(request):
    item_id = 1
    api_data = get_external_api_data(item_id)
    return render(request, 'example/external_api_cached.html', {'api_data': api_data})


def external_api_uncached_view(request):
    item_id = 1
    api_data = get_external_api_data(item_id, False)
    return render(request, 'example/external_api_cached.html', {'api_data': api_data})
