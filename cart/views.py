# Django
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.contrib.humanize.templatetags.humanize import intcomma

# local Django
from .models import Cart, CartItem
from .utils import get_cart_id, get_cart_items, cart_summery
from store.models import Variant
from .context_processors import cart_items_count


# Create your views here.


def user_cart(request):
    cart_items = get_cart_items(request)
    result = cart_summery(request)  # Get cart summery with total price, tax, grand total

    context = {
        'cart_items': cart_items,
        'total': result['total_price'],
        'tax': result['tax'],
        'grand_total': result['grand_total']
    }

    return render(request, 'cart/cart.html', context)


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


def increment_cart_item(request, cart_item_id):
    if request.is_ajax():
        cart_item = CartItem.objects.get(pk=cart_item_id)
        cart_item.quantity += 1
        cart_item.save()
        quantity = cart_item.quantity
        sub_total = cart_item.sub_total()

        cart_count = cart_items_count(request)  # Get cart count
        result = cart_summery(request)  # Get cart summery with total price, tax, grand total

        context = {
            'quantity': quantity,
            'sub_total': intcomma(sub_total),
            'tax': intcomma(result['tax']),
            'total': intcomma(result['total_price']),
            'grand_total': intcomma(result['grand_total']),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


def decrement_cart_item(request, cart_item_id):
    if request.is_ajax():
        # Cart item decrementing
        cart_item = CartItem.objects.get(pk=cart_item_id)
        cart_item.quantity -= 1
        cart_item.save()
        quantity = cart_item.quantity
        sub_total = cart_item.sub_total()

        result = cart_summery(request)  # Get cart summery with total price, tax, grand total
        cart_count = cart_items_count(request)  # Get cart count

        context = {
            'quantity': quantity,
            'sub_total': intcomma(sub_total),
            'tax': intcomma(result['tax']),
            'total': intcomma(result['total_price']),
            'grand_total': intcomma(result['grand_total']),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


def delete_cart_item(request, cart_item_id):
    if request.is_ajax():
        CartItem.objects.get(pk=cart_item_id).delete()

        cart_count = cart_items_count(request)
        result = cart_summery(request)  # Get cart summery with total price, tax, grand total

        context = {
            'tax': intcomma(result['tax']),
            'total': intcomma(result['total_price']),
            'grand_total': intcomma(result['grand_total']),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


def checkout(request):
    return render(request, 'cart/checkout.html')
