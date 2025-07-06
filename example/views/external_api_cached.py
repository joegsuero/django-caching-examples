import time
import requests
from django.shortcuts import render
from django.core.cache import cache
from example.models import Product


# --- 3. Useful Antipattern: Caching External APIs ---
# A simple public API for mock
EXTERNAL_API_MOCK_URL = "https://jsonplaceholder.typicode.com/posts/1"


def get_external_api_data(item_id):
    """Simulates a slow external API call."""
    cache_key = f'external_api_data_{item_id}'
    data = cache.get(cache_key)

    if data is None:
        print(f"--- Getting external API data for {item_id} (no cache) ---")
        try:
            # Simulate real network latency
            start_time = time.time()
            # You could make item_id dynamic here
            response = requests.get(f'{EXTERNAL_API_MOCK_URL}')
            end_time = time.time()
            print(
                f"   External API latency: {end_time - start_time:.2f} seconds")

            response.raise_for_status()
            data = response.json()
            cache.set(cache_key, data, timeout=60 * 60)  # Cache for 1 hour
        except requests.exceptions.RequestException as e:
            print(f"Error getting external API data: {e}")
            data = {"error": "Could not retrieve external data."}
    else:
        print(f"--- Getting external API data for {item_id} (from cache) ---")
    return data


def external_api_cached_view(request):
    item_id = 1  # For this example, always item 1
    api_data = get_external_api_data(item_id)
    return render(request, 'myapp/external_api_cached.html', {'api_data': api_data})
