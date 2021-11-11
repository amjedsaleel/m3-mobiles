# django
from django.shortcuts import render, redirect
from django.contrib import messages

# local Django
from brand.models import Brand
from brand.forms import BrandForm
from store.models import Product

# Create your views here.


def dashboard(request):
    return render(request, 'adminPanel/dashboard.html')


def brand(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'adminPanel/brand.html', context)


def add_brand(request):
    form = BrandForm(use_required_attribute=False)

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, use_required_attribute=False)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added new brand')
            return redirect('admin-panel:brand')

    context = {
        'form': form
    }
    return render(request, 'adminPanel/add-brand.html', context)


def product(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'adminPanel/product-list.html', context)


def product_add(request):
    return render(request, 'adminPanel/product-add.html')
