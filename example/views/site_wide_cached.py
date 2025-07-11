from datetime import datetime
from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from example.utils import heavy_computation
from example.models import Product


# --- (Requires Middleware) ---
# This view is simple, but will demonstrate Site-Wide Caching if the middleware is active.
def site_wide_cached_view(request):
    print("--- Executing site_wide_cached_view ---")
    heavy_computation(0.3)
    products_count = Product.objects.count()
    return render(request, 'example/site_wide_cached.html', {
        'products_count': products_count,
        'current_time': datetime.now()
    })
