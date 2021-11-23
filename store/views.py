# Django
from django.shortcuts import render

# local Django
from .models import Variant
from brand.models import Brand

# Create your views here.


def index(request):
    last_products = Variant.objects.all()[:6]
    brands = Brand.objects.all()
    context = {
        'last_products': last_products,
        'brands': brands
    }
    return render(request, 'store/index.html', context)


def store(request):
    brands = Brand.objects.all()
    variants = Variant.objects.all()
    variants_count = variants.count()
    context = {
        'brands': brands,
        'variants': variants,
        'variants_count': variants_count
    }
    return render(request, 'store/store.html', context)


def brand_wise(request, brand_slug):
    variants = Variant.objects.filter(product__brand__slug=brand_slug)
    variants_count = variants.count()
    brands = Brand.objects.all()
    context = {
        'brands': brands,
        'variants': variants,
        'variants_count': variants_count
    }
    return render(request, 'store/store.html', context)


def product_details(request, brand_slug, variant_slug):
    variant = Variant.objects.get(slug=variant_slug)
    suggestions = Variant.objects.filter(product_id=variant.product.id)
    context = {
        'variant': variant,
        'suggestions': suggestions
    }
    return render(request, 'store/product-details.html', context)
