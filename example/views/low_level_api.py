from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from example.utils import heavy_computation
from example.models import Product


# --- 2. Low-Level Cache API ---
def get_heavy_data_from_db(param1, param2):
    """Simulates a complex query or calculation."""
    cache_key = f"heavy_db_data_{param1}_{param2}"
    data = cache.get(cache_key)

    if data is None:
        print(f"--- Calculating heavy data for {param1}, {param2} (DB) ---")
        heavy_computation(0.7)  # Simulate very heavy query
        # Retrieve DB data and convert to dicts to cache serializable data
        data = list(Product.objects.filter(category__name__icontains=param1, price__gt=param2)
                    .values('name', 'price', 'category__name'))
        cache.set(cache_key, data, timeout=60 * 10)  # Cache for 10 minutes
    else:
        print(
            f"--- Getting heavy data for {param1}, {param2} (from cache) ---")
    return data


def low_level_api_view(request):
    param1 = request.GET.get('cat', 'Electronics')
    param2 = float(request.GET.get('price_gt', 50.00))

    data = get_heavy_data_from_db(param1, param2)
    return render(request, 'myapp/low_level_api.html', {
        'data': data,
        'param1': param1,
        'param2': param2
    })
