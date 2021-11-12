# django
from django.shortcuts import render, redirect
from django.contrib import messages

# local Django
from brand.models import Brand
from brand.forms import BrandForm
from store.models import Variant
from store.forms import VariantForm, ProductForm

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


def all_products(request):
    variants = Variant.objects.all()
    context = {
        'variants': variants
    }
    return render(request, 'adminPanel/product-list.html', context)


def add_product(request):
    form = ProductForm(use_required_attribute=False)

    if request.method == 'POST':
        form = ProductForm(request.POST, use_required_attribute=False)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully new product added')
            return redirect('admin-panel:products')

    context = {
        'form': form
    }
    return render(request, 'adminPanel/product-add.html', context)


def add_variant(request):
    form = VariantForm(use_required_attribute=False)

    if request.method == 'POST':
        form = VariantForm(request.POST, request.FILES, use_required_attribute=False)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully new product variant added')
            return redirect('admin-panel:products')

    context = {
        'form': form
    }
    return render(request, 'adminPanel/add-variants.html', context)
