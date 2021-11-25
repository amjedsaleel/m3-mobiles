# local Django
from .models import CartItem


def get_cart_id(request):
    """
    Get cart id. If cart is not exists create new cart with session key
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def get_cart_items(request):
    """
    Filter cart items based on the user
    """
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(cart__cart_id=get_cart_id(request))
    return cart_items


def cart_summery(request):
    """
    Calculating cart summery.
    Total price, tax, and grand total.
    """
    cart_items = get_cart_items(request)
    total = 0
    tax = 0
    for cart_item in cart_items:
        total += cart_item.variant.mrp * cart_item.quantity
        tax += cart_item.variant.tax * cart_item.quantity

    grand_total = tax + total

    request.session['total_price'] = total
    request.session['tax'] = tax
    request.session['grand_total'] = grand_total

