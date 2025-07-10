from datetime import datetime
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from example.models import Product
from example.utils import heavy_computation


# --- 1. Per-View Caching ---
@cache_page(60 * 5)  # Cache for 5 minutes
def per_view_cached_products(request):
    """
    View that simulates a heavy DB query and template rendering.
    Demonstrates the effect of the @cache_page decorator.
    """
    print("--- Executing per_view_cached_products (no cache) ---")
    heavy_computation(0.5)  # Simulate a DB query or complex logic
    products = Product.objects.select_related(
        'category').filter(is_active=True)[:10]
    context = {
        'products': products,
        'current_time': datetime.now(),
        'cached_status': 'NO CACHE (COMPARISON)'
    }
    return render(request, 'example/per_view_cached.html', context)


def template_fragment_demo_view(request):
    latest_news = ["Headline A: Simulated heavy content",
                   "Headline B: More data here"]
    return render(request, 'example/template_fragment_cached.html', {
        'latest_news': latest_news,
        'current_time': datetime.now(),
        'cached_news_time': datetime.now()  # To show when the news cache was generated
    })


def per_view_uncached_products(request):
    """
    Similar view to the above, but without caching, for performance comparison.
    """
    print("--- Executing per_view_uncached_products (full execution) ---")
    heavy_computation(0.5)
    products = Product.objects.select_related(
        'category').filter(is_active=True)[:10]
    context = {
        'products': products,
        'current_time': datetime.now(),
        'cached_status': 'NO CACHE'
    }
    return render(request, 'example/per_view_cached.html', context)
