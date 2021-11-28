# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


# local Django
from .decorators import admin_only
from brand.models import Brand
from brand.forms import BrandForm
from store.models import Product, Variant
from store.forms import VariantForm, ProductForm
from order.models import OrderProduct, STATUS
from offer.models import VariantOffer, ProductOffer, BrandOffer
from offer.froms import VariantOfferForm, ProductOfferForm, BrandOfferForm

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
@admin_only
def dashboard(request):
    return render(request, 'adminPanel/dashboard.html')


@never_cache
@admin_only
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
@admin_only
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
@admin_only
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
@admin_only
def delete_brand(request, brand_id):
    """
    Delete the brand
    """
    if request.is_ajax():
        Brand.objects.get(pk=brand_id).delete()
        return JsonResponse({'message': 'success'})

    return redirect('admin-panel:products')


@never_cache
@admin_only
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
@admin_only
def delete_product(request, product_id):
    """
    Delete the product
    """
    if request.is_ajax():
        print('Delete product')
        Product.objects.get(pk=product_id).delete()
        return JsonResponse({'message': 'success'})


@never_cache
@admin_only
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
@admin_only
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
@admin_only
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
@admin_only
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
@admin_only
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
@admin_only
def delete_variant(request, variant_id):
    """
    Delete a variant
    """
    if request.is_ajax():
        Variant.objects.get(pk=variant_id).delete()
        return JsonResponse({'message': 'success'})
    return redirect('admin-panel:products')


@never_cache
@admin_only
def variant_details(request, variant_slug):
    return render(request, 'adminPanel/variant-detail.html')


@never_cache
@admin_only
def users_list(request):
    users = User.objects.all()
    return render(request, 'adminPanel/users.html', {'users': users})


@never_cache
@admin_only
def block_user(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return JsonResponse({'message': 'success'})


@never_cache
@admin_only
def unblock_user(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return JsonResponse({'message': 'success'})


@never_cache
@admin_only
def active_order_products(request):
    exclude_list = ['Delivered', 'Canceled']
    active_orders = OrderProduct.objects.all().exclude(status__in=exclude_list)
    status = STATUS
    context = {
        'active_orders': active_orders,
        'status': status
    }
    return render(request, 'adminPanel/active-orders.html', context)


@never_cache
@admin_only
def update_order_status(request, pk):
    if request.method == 'POST':
        status = request.POST.get('status')
        order_product = OrderProduct.objects.get(pk=pk)

        if status == 'Canceled':
            variant = order_product.variant
            variant.stock += order_product.quantity
            variant.save()

        order_product.status = status
        order_product.save()
        return JsonResponse({'message': status})


@never_cache
@admin_only
def order_history(request):
    orders = OrderProduct.objects.filter(status__in=['Delivered', 'Canceled']).order_by('-tracking_id')
    return render(request, 'adminPanel/order-history.html', {'orders': orders})


@never_cache
@admin_only
def offers(request):
    variant_offers = VariantOffer.objects.all()
    product_offers = ProductOffer.objects.all()
    brand_offers = BrandOffer.objects.all()

    context = {
        'variant_offers': variant_offers,
        'product_offers': product_offers,
        'brand_offers': brand_offers
    }
    return render(request, 'adminPanel/offers.html', context)


@never_cache
@admin_only
def add_variant_offer(request):
    form = VariantOfferForm()

    if request.method == 'POST':
        form = VariantOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New variant offer added")
            return redirect('admin-panel:offers')

    return render(request, 'adminPanel/add-offer.html', {'form': form})


@never_cache
@admin_only
def add_product_offer(request):
    form = ProductOfferForm()

    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New product offer added")
            return redirect('admin-panel:offers')

    return render(request, 'adminPanel/add-offer.html', {'form': form})


@never_cache
@admin_only
def add_brand_offer(request):
    form = BrandOfferForm()

    if request.method == 'POST':
        form = BrandOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New brand offer was added")
            return redirect('admin-panel:offers')

    return render(request, 'adminPanel/add-offer.html', {'form': form})


@never_cache
@admin_only
def update_variant_offer(request, pk):
    variant_offer = VariantOffer.objects.get(pk=pk)
    form = VariantOfferForm(instance=variant_offer)

    if request.method == 'POST':
        form = VariantOfferForm(request.POST, instance=variant_offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Variant offer was updated')
            return redirect('admin-panel:offers')

    return render(request, 'adminPanel/update-offer.html', {'form': form})


@never_cache
@admin_only
def update_product_offer(request, pk):
    product_offer = ProductOffer.objects.get(pk=pk)
    form = ProductOfferForm(instance=product_offer)

    if request.method == 'POST':
        form = ProductOfferForm(request.POST, instance=product_offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product offer was updated')
            return redirect('admin-panel:offers')

    return render(request, 'adminPanel/update-offer.html', {'form': form})


@never_cache
@admin_only
def update_brand_offer(request, pk):
    brand_offer = BrandOffer.objects.get(pk=pk)
    form = BrandOfferForm(instance=brand_offer)

    if request.method == 'POST':
        form = BrandOfferForm(request.POST, instance=brand_offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand offer was updated')
            return redirect('admin-panel:offers')

    return render(request, 'adminPanel/update-offer.html', {'form': form})


@never_cache
@admin_only
def delete_variant_offer(request, pk):

    if request.method == 'POST':
        VariantOffer.objects.get(pk=pk).delete()
        return JsonResponse({'message': "success"})

    return redirect('admin-panel:offers')


@never_cache
@admin_only
def delete_product_offer(request, pk):

    if request.method == 'POST':
        ProductOffer.objects.get(pk=pk).delete()
        return JsonResponse({'message': "success"})

    return redirect('admin-panel:offers')


@never_cache
@admin_only
def delete_brand_offer(request, pk):

    if request.method == 'POST':
        BrandOffer.objects.get(pk=pk).delete()
        return JsonResponse({'message': "success"})

    return redirect('admin-panel:offers')
