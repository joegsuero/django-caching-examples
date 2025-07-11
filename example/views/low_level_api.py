from django.shortcuts import render
from django.core.cache import cache

from example.utils import heavy_computation
from example.models import Product


def get_heavy_data_from_db(param1, param2, enable_cache=True):
    """Simulates a complex query or calculation."""
    cache_key = f"heavy_db_data_{param1}_{param2}"
    data = cache.get(cache_key) if enable_cache else None

    if data is None:
        print(f"--- Calculating heavy data for {param1}, {param2} (DB) ---")
        heavy_computation(0.7)
        data = list(Product.objects.filter(category__name__icontains=param1, price__gt=param2)
                    .values('name', 'price', 'category__name'))
        if enable_cache:
            cache.set(cache_key, data, timeout=60 * 10)
    else:
        print(
            f"--- Getting heavy data for {param1}, {param2} (from cache) ---")
    return data


def low_level_api_view(request):
    param1 = request.GET.get('cat', 'Electronics')
    param2 = float(request.GET.get('price_gt', 50.00))

    data = get_heavy_data_from_db(param1, param2)
    return render(request, 'example/low_level_api.html', {
        'data': data,
        'param1': param1,
        'param2': param2
    })


def low_level_api_view_uncached(request):
    param1 = request.GET.get('cat', 'Electronics')
    param2 = float(request.GET.get('price_gt', 50.00))

    data = get_heavy_data_from_db(param1, param2, enable_cache=False)
    return render(request, 'example/low_level_api.html', {
        'data': data,
        'param1': param1,
        'param2': param2
    })
