# Django
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404

# local Django
from .models import Cart, CartItem
from .utils import get_cart_id
from store.models import Variant


# Create your views here.


def cart(request):
    cart_items = CartItem.objects.filter(cart__cart_id=get_cart_id(request))

    context = {
        'cart_items': cart_items
    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, variant_slug):
    if request.is_ajax():

        variant = Variant.objects.get(slug=variant_slug)

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
            return JsonResponse({'message': 'success'})
        except CartItem.DoesNotExist:
            """ Adding new item to cart"""
            cart_item = CartItem.objects.create(cart=cart, variant=variant, quantity=1)
            cart_item.save()
            return JsonResponse({'message': 'success'})
    raise Http404
