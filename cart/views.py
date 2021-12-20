# Django
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

# local Django
from .models import Cart, CartItem
from .utils import get_cart_id, get_cart_items, cart_summery
from .context_processors import cart_items_count
from store.models import Variant
from order.forms import OrderForm
from userProfile.models import Address


# Create your views here.


def user_cart(request):
    cart_items = get_cart_items(request)
    cart_summery(request)  # Get cart summery with total price, tax, grand total

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)


@csrf_exempt
def add_to_cart(request, variant_slug):
    if request.is_ajax():
        variant = Variant.objects.get(slug=variant_slug)

        if request.user.is_authenticated:  # Adding cart items to logged users
            try:
                """ Fetching the cart with session key """
                cart = Cart.objects.get(cart_id=get_cart_id(request))
            except Cart.DoesNotExist:
                """ Creating new cart """
                cart = Cart.objects.create(cart_id=get_cart_id(request))
                cart.save()

            try:
                """ Incrementing existing cart item quantity """
                cart_item = CartItem.objects.get(user=request.user, variant=variant)
                cart_item.quantity += 1
                cart_item.save()
                cart_count = cart_items_count(request)
                return JsonResponse({'cart_count': cart_count['count']})
            except CartItem.DoesNotExist:
                """ Adding new item to cart"""
                cart_item = CartItem.objects.create(user=request.user, variant=variant, quantity=1, cart=cart)
                cart_item.save()
                cart_count = cart_items_count(request)

                return JsonResponse({'cart_count': cart_count['count']})

        else:  # Adding cart items to not logged user
            try:
                """ Fetching the cart with session key """
                cart = Cart.objects.get(cart_id=get_cart_id(request))
            except Cart.DoesNotExist:
                """ Creating new cart """
                cart = Cart.objects.create(cart_id=get_cart_id(request))
                cart.save()

            try:
                """ Incrementing existing cart item quantity """
                cart_item = CartItem.objects.get(cart=cart, variant=variant)
                cart_item.quantity += 1
                cart_item.save()
                cart_count = cart_items_count(request)

                return JsonResponse({'cart_count': cart_count['count']})
            except CartItem.DoesNotExist:
                """ Adding new item to cart"""
                cart_item = CartItem.objects.create(cart=cart, variant=variant, quantity=1)
                cart_item.save()
                cart_count = cart_items_count(request)

                return JsonResponse({'cart_count': cart_count['count']})
    raise Http404


@csrf_exempt
def increment_cart_item(request, cart_item_id):
    if request.is_ajax():
        cart_item = CartItem.objects.get(pk=cart_item_id)
        cart_item.quantity += 1
        cart_item.save()
        quantity = cart_item.quantity
        sub_total = cart_item.sub_total()

        cart_count = cart_items_count(request)  # Get cart count
        cart_summery(request)  # Get cart summery with total price, tax, grand total

        context = {
            'quantity': quantity,
            'sub_total': intcomma(sub_total),
            'tax': intcomma(request.session['tax']),
            'total': intcomma(request.session['total_price']),
            'grand_total': intcomma(request.session['grand_total']),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


@csrf_exempt
def decrement_cart_item(request, cart_item_id):
    if request.is_ajax():
        # Cart item decrementing
        cart_item = CartItem.objects.get(pk=cart_item_id)
        cart_item.quantity -= 1
        cart_item.save()
        quantity = cart_item.quantity
        sub_total = cart_item.sub_total()

        cart_summery(request)  # Get cart summery with total price, tax, grand total
        cart_count = cart_items_count(request)  # Get cart count

        context = {
            'quantity': quantity,
            'sub_total': intcomma(sub_total),
            'tax': intcomma(request.session['tax']),
            'total': intcomma(request.session['total_price']),
            'grand_total': intcomma(request.session['grand_total']),
            'cart_count': cart_count['count']
        }
        return JsonResponse(context)


@csrf_exempt
def delete_cart_item(request, cart_item_id):
    if request.is_ajax():
        CartItem.objects.get(pk=cart_item_id).delete()
        cart_count = cart_items_count(request)
        cart_summery(request)  # Get cart summery with total price, tax, grand total

        context = {
            'tax': intcomma(request.session['tax']),
            'total': intcomma(request.session['total_price']),
            'grand_total': intcomma(request.session['grand_total']),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


@login_required
def checkout(request):
    try:
        del request.session['coupon_code']
    except KeyError:
        pass

    cart_summery(request)
    addresses = Address.objects.filter(user=request.user)
    try:
        default_address = addresses.get(default=True)
        form = OrderForm(
            initial={
                'full_name': default_address.full_name,
                'phone': default_address.phone,
                'email': default_address.email,
                'house_no': default_address.house_no,
                'area': default_address.area,
                'landmark': default_address.landmark,
                'town': default_address.town,
                'state': default_address.state,
                'pin': default_address.pin
            }
        )
    except ObjectDoesNotExist:
        form = OrderForm()

    context = {
        'from': form,
        'addresses': addresses,
        'tax': intcomma(request.session['tax']),
        'total': intcomma(request.session['total_price']),
        'grand_total': intcomma(request.session['grand_total']),
    }
    return render(request, 'cart/checkout.html', context)


@login_required
def buy_now_checkout(request):
    try:
        del request.session['coupon_code']
    except KeyError:
        pass

    try:
        variant = Variant.objects.get(slug=request.GET.get('variant'))
    except Variant.DoesNotExist:
        return redirect('store:store')

    addresses = Address.objects.filter(user=request.user)

    try:
        default_address = addresses.get(default=True)
        form = OrderForm(
            initial={
                'full_name': default_address.full_name,
                'phone': default_address.phone,
                'email': default_address.email,
                'house_no': default_address.house_no,
                'area': default_address.area,
                'landmark': default_address.landmark,
                'town': default_address.town,
                'state': default_address.state,
                'pin': default_address.pin
            }
        )
    except ObjectDoesNotExist:
        form = OrderForm()

    total = variant.mrp
    tax = variant.tax
    grand_total = total + tax
    context = {
        'from': form,
        'addresses': addresses,
        'tax': intcomma(tax),
        'total': intcomma(total),
        'grand_total': intcomma(grand_total),
        'variant_slug': variant.slug
    }
    return render(request, 'cart/buy-now-checkout.html', context)
