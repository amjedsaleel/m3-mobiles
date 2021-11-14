# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

# local Django
from brand.models import Brand
from brand.forms import BrandForm
from store.models import Product, Variant
from store.forms import VariantForm, ProductForm
from .decorators import admin_ony

User = get_user_model()

# Create your views here.


def admin_login(request):
    if 'admin' in request.session:
        return redirect('admin-panel:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_superuser:
                request.session['admin'] = 'admin'
                return redirect('admin-panel:dashboard')

        messages.error(request, 'Invalid credentials')
        return redirect('admin-panel:login')
    return render(request, 'adminPanel/sign-in.html')


def logout(request):
    del request.session['admin']
    return redirect('admin-panel:login')


@never_cache
@admin_ony
def dashboard(request):
    return render(request, 'adminPanel/dashboard.html')


@never_cache
@admin_ony
def brand(request):
    """
    Listing all brands
    """
    brands = Brand.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'adminPanel/brand.html', context)


@never_cache
@admin_ony
def add_brand(request):
    """
    Adding new brand
    """
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


@never_cache
@admin_ony
def edit_brand(request, brand_id):
    """
    Edit / Update an existing brand
    """
    brand = Brand.objects.get(pk=brand_id)
    form = BrandForm(instance=brand, use_required_attribute=False)

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand, use_required_attribute=False)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully brand updated')
            return redirect('admin-panel:brand')

    context = {
        'form': form,
    }
    return render(request, 'adminPanel/edit-brand.html', context)


@never_cache
@admin_ony
def delete_brand(request, brand_id):
    """
    Delete the brand
    """
    if request.is_ajax():
        Brand.objects.get(pk=brand_id).delete()
        return JsonResponse({'message': 'success'})

    return redirect('admin-panel:products')


@never_cache
@admin_ony
def all_products(request):
    """
    Listing all products and variants
    """
    products = Product.objects.all()
    variants = Variant.objects.all()
    context = {
        'variants': variants,
        'products': products
    }
    return render(request, 'adminPanel/product-list.html', context)


@never_cache
@admin_ony
def delete_product(request, product_id):
    """
    Delete the product
    """
    if request.is_ajax():
        print('Delete product')
        Product.objects.get(pk=product_id).delete()
        return JsonResponse({'message': 'success'})


def edit_product(request, product_id):
    """
    Edit/Update the product
    """
    product = Product.objects.get(pk=product_id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully product updated')
            return redirect('admin-panel:products')

    context = {
        'form': form
    }
    return render(request, 'adminPanel/edit-product.html', context)


@never_cache
@admin_ony
def brand_wise_variant(request, variant_id):
    """
    Filter variants based on the brand
    """
    variants = Variant.objects.filter(product__brand__slug=variant_id)
    context = {
        'variants': variants
    }
    return render(request, 'adminPanel/product-list.html', context)


@never_cache
@admin_ony
def add_product(request):
    """
    Adding new product
    """
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


@never_cache
@admin_ony
def add_variant(request):
    """
    Adding new variant under a product
    """
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


@never_cache
@admin_ony
def edit_variant(request, variant_id):
    """
    Edit/Update variants
    """
    variant = Variant.objects.get(pk=variant_id)
    form = VariantForm(instance=variant, use_required_attribute=False)

    if request.method == 'POST':
        form = VariantForm(request.POST, request.FILES, instance=variant)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated')
            return redirect('admin-panel:products')

    context = {
        'form': form
    }
    return render(request, 'adminPanel/edit-variant.html', context)


@never_cache
def delete_variant(request, variant_id):
    """
    Delete a variant
    """
    if request.is_ajax():
        Variant.objects.get(pk=variant_id).delete()
        return JsonResponse({'message': 'success'})
    return redirect('admin-panel:products')
