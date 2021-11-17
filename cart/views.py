# Django
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.contrib.humanize.templatetags.humanize import intcomma

# local Django
from .models import Cart, CartItem
from .utils import get_cart_id, get_cart_items
from store.models import Variant
from .context_processors import cart_items_count


# Create your views here.


def user_cart(request):
    cart_items = get_cart_items(request)

    total = 0
    for cart_item in cart_items:
        total += cart_item.variant.price * cart_item.quantity

    tax = (18 * total) / 100
    grand_total = tax + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
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

        cart_items = get_cart_items(request)

        total = 0
        for i in cart_items:
            total += i.variant.price * i.quantity

        tax = (18 * total) / 100
        grand_total = tax + total
        cart_count = cart_items_count(request)

        context = {
            'quantity': quantity,
            'sub_total': intcomma(sub_total),
            'tax': intcomma(tax),
            'total': intcomma(total),
            'grand_total': intcomma(grand_total),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


def decrement_cart_item(request, cart_item_id):
    if request.is_ajax():
        print('decrement')
        cart_item = CartItem.objects.get(pk=cart_item_id)
        cart_item.quantity -= 1
        cart_item.save()
        quantity = cart_item.quantity
        sub_total = cart_item.sub_total()

        cart_items = get_cart_items(request)

        total = 0
        for i in cart_items:
            total += i.variant.price * i.quantity

        tax = (18 * total) / 100
        grand_total = tax + total
        cart_count = cart_items_count(request)

        context = {
            'quantity': quantity,
            'sub_total': intcomma(sub_total),
            'tax': intcomma(tax),
            'total': intcomma(total),
            'grand_total': intcomma(grand_total),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


def delete_cart_item(request, cart_item_id):
    if request.is_ajax():
        CartItem.objects.get(pk=cart_item_id).delete()

        cart_items = get_cart_items(request)

        total = 0
        for i in cart_items:
            total += i.variant.price * i.quantity

        tax = (18 * total) / 100
        grand_total = tax + total
        cart_count = cart_items_count(request)

        context = {
            'tax': intcomma(tax),
            'total': intcomma(total),
            'grand_total': intcomma(grand_total),
            'cart_count': cart_count['count']
        }

        return JsonResponse(context)


def checkout(request):
    return render(request, 'cart/checkout.html')
