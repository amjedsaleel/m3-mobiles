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
