from django.urls import path
from . import views

urlpatterns = [
    path('products/cached/', views.per_view_cached_products,
         name='per_view_cached_products'),
    path('products/uncached/', views.per_view_uncached_products,
         name='per_view_uncached_products'),
    path('low-level-cache/', views.low_level_api_view, name='low_level_api_view'),
    path('external-api-cached/', views.external_api_cached_view,
         name='external_api_cached_view'),
    path('site-wide-cached/', views.site_wide_cached_view,
         name='site_wide_cached_view'),
    path('template-fragment-cache/', views.template_fragment_demo_view,
         name='template_fragment_demo'),
]
