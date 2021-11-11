# django
from django.shortcuts import render

# local Django
from brand.models import Brand

# Create your views here.


def dashboard(request):
    return render(request, 'adminPanel/dashboard.html')


def brand(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'adminPanel/brand.html', context)
