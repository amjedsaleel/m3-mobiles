# started library
import datetime
import csv

# third party
import weasyprint

# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string

# local Django
from .decorators import admin_only
from accounts.models import CustomUser
from brand.models import Brand
from brand.forms import BrandForm
from store.models import Product, Variant
from store.forms import VariantForm, ProductForm
from payment.models import Payment
from order.models import OrderProduct, STATUS, Order
from offer.models import VariantOffer, ProductOffer, BrandOffer, Coupon, RedeemedCoupon
from offer.froms import VariantOfferForm, ProductOfferForm, BrandOfferForm, CouponFrom

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
    current_year = timezone.now().year
    variants = Variant.objects.all()
    brands = Brand.objects.all()
    order_products = OrderProduct.objects.all()

    total_orders = Order.objects.filter(is_ordered=True).count()
    total_users = CustomUser.objects.all().count()
    total_revenue = Order.objects.aggregate(Sum('order_total'))

    landing_price_sum = Variant.objects.aggregate(Sum('landing_price'))
    total_landing_price = landing_price_sum['landing_price__sum']
    total_profit = float(total_revenue['order_total__sum']) - float(total_landing_price)

    order_products = OrderProduct.objects.filter(created_at__lt=datetime.date(current_year, 12, 31), status='Delivered')
    month_wise_order_count = list()
    mount = timezone.now().month
    for i in range(1, mount + 1):
        month_wise_order = order_products.filter(created_at__month=i).count()
        month_wise_order_count.append(month_wise_order)

    cod_count = Payment.objects.filter(payment_method='COD').count()
    paypal_count = Payment.objects.filter(payment_method="PayPal").count()
    razorpay_count = Payment.objects.filter(payment_method='razorpay').count()

    brands_list = list()
    products_count = list()
    for i in brands:
        brands_list.append(i.name)
        products_count.append(Variant.objects.filter(product__brand__name=i.name).count())

    most_moving_brands_count = list()
    most_moving_brands = list()
    for i in brands:
        most_moving_brands.append(i)
        most_moving_brands_count.append(
            OrderProduct.objects.filter(variant__product__brand=i, status="Delivered").count())

    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_revenue': total_revenue['order_total__sum'],
        'total_profit': total_profit,

        'month_wise_order_count': month_wise_order_count,
        'month_name': ['January', 'February', 'March', 'May', 'June', 'July', 'August', 'September', 'October',
                       'November', 'December'],

        'payment_method_status': [cod_count, paypal_count, razorpay_count],

        'brands_list': brands_list,
        'products_count': products_count,

        'most_moving_brands': most_moving_brands,
        'most_moving_brands_count': most_moving_brands_count,
    }
    return render(request, 'adminPanel/dashboard.html', context)


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
    orders = OrderProduct.objects.filter(status__in=['Delivered', 'Canceled'])
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


@admin_only
def coupons(request):
    all_coupons = Coupon.objects.all().order_by('-created_at')
    context = {
        'all_coupons': all_coupons
    }
    return render(request, 'adminPanel/coupons.html', context)


@admin_only
def add_coupon(request):
    form = CouponFrom()

    if request.method == 'POST':
        form = CouponFrom(request.POST)
        if form.is_valid():
            print('yes')
            form.save()
            messages.success(request, 'New coupon is added')
            return redirect('admin-panel:all-coupons')
    return render(request, 'adminPanel/add-coupon.html', {'form': form})


@admin_only
def edit_coupon(request, pk):
    coupon = Coupon.objects.get(pk=pk)
    form = CouponFrom(instance=coupon)

    if request.method == 'POST':
        form = CouponFrom(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon was successfully updated')
            return redirect('admin-panel:all-coupons')
    return render(request, 'adminPanel/edit-coupon.html', {'form': form})


@admin_only
def delete_coupon(request, pk):
    if request.method == 'POST':
        Coupon.objects.get(pk=pk).delete()
        return JsonResponse({'message': 'success'})


@admin_only
def redeemed_coupon(request):
    redeemed_coupons = RedeemedCoupon.objects.all().order_by('-created_at')

    context = {
        'redeemed_coupons': redeemed_coupons
    }
    return render(request, 'adminPanel/redeemed-coupons.html', context)


@admin_only
def report(request):
    brands = Brand.objects.all()
    variants = Variant.objects.all()
    order_products = OrderProduct.objects.all()

    if request.GET.get('from'):
        date_from = datetime.datetime.strptime(request.GET.get('from'), "%Y-%m-%d")
        date_to = datetime.datetime.strptime(request.GET.get('to'), "%Y-%m-%d")
        date_to += datetime.timedelta(days=1)
        order_products = order_products.filter(created_at__range=[date_from, date_to])

    context = {
        'brands': brands,
        'variants': variants,
        'order_products': order_products,
    }
    return render(request, 'adminPanel/report.html', context)


@admin_only
def order_product_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'

    writer = csv.writer(response)
    order_products = OrderProduct.objects.all()

    writer.writerow(
        ['Customer', 'Tracking Id', 'product', 'variant', 'Quantity', 'Amount paid', 'Discount', 'Date', 'status'])

    for order_product in order_products:
        writer.writerow([order_product.user.first_name, order_product.tracking_id, order_product.variant.product.name,
                         order_product.variant.get_variant(), order_product.quantity, order_product.paid,
                         order_product.discount, order_product.created_at, order_product.status])
    return response


@admin_only
def brands_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=brands.csv'
    writer = csv.writer(response)
    writer.writerow(['Brand name'])
    brands = Brand.objects.all()

    for i in brands:
        writer.writerow([i.name])

    return response


@admin_only
def all_variants_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-products.csv'
    writer = csv.writer(response)
    writer.writerow(['Product', 'Brand', 'Variant', 'Landing price', 'M.R.P', 'Tax', 'Stock'])

    all_variants = Variant.objects.all()
    for i in all_variants:
        writer.writerow(
            [i.product.name, i.product.brand.name, i.get_variant(), i.landing_price, i.mrp, i.tax, i.stock])

    return response


@admin_only
def brand_pdf(request):
    brands = Brand.objects.all()
    html = render_to_string('adminPanel/brand-pdf.html', {'brands': brands})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=brands.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


@admin_only
def order_products_pdf(request):
    order_products = OrderProduct.objects.all()
    html = render_to_string('adminPanel/order-products-pdf.html', {'order_products': order_products})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=orders.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


@admin_only
def all_variants_pdf(request):
    variants = Variant.objects.all()
    html = render_to_string('adminPanel/all-varinats-pdf.html', {'variants': variants})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=all_products.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
