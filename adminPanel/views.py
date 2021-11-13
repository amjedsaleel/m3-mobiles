# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import JsonResponse

# local Django
from brand.models import Brand
from brand.forms import BrandForm
from store.models import Variant
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


@admin_ony
def dashboard(request):
    return render(request, 'adminPanel/dashboard.html')


@admin_ony
def brand(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'adminPanel/brand.html', context)


@admin_ony
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


@admin_ony
def all_products(request):
    variants = Variant.objects.all()
    context = {
        'variants': variants
    }
    return render(request, 'adminPanel/product-list.html', context)


@admin_ony
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


@admin_ony
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


def delete_variant(request, id):
    if request.is_ajax():
        Variant.objects.get(pk=id).delete()
        return JsonResponse({'message': 'success'})
    return redirect('admin-panel:products')
