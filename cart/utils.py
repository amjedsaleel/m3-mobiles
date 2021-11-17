# local Django
from .models import CartItem


def get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def get_cart_items(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(cart__cart_id=get_cart_id(request))
    return cart_items
