# local Django
from .models import Order, OrderProduct
from cart.models import CartItem, Cart, Variant
from cart.utils import get_cart_id
from payment.models import Payment


def make_order(request):
    payment = Payment.objects.get(id=request.session['payment_id'])

    # Creating Order
    order = Order.objects.create(
        user=request.user,
        payment=payment,
        full_name=request.session['full_name'],
        phone=request.session['phone'],
        email=request.session['email'],
        house_no=request.session['house_no'],
        area=request.session['area'],
        landmark=request.session['landmark'],
        town=request.session['town'],
        state=request.session['state'],
        pin=request.session['pin'],
        is_ordered=True,
        order_total=request.session['total_price'],
        tax=request.session['tax'],
        grand_total=request.session['grand_total']
    )

    # Saving ordered products
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = OrderProduct.objects.create(
            user=request.user,
            order=order,
            payment=payment,
            variant=item.variant,
            quantity=item.quantity,
            price=item.variant.price,
            ordered=True,
        )

        # Decrease the stock
        variant = Variant.objects.get(pk=item.variant.id)
        variant.stock -= item.quantity
        variant.save()

    # Delete user cart
    try:
        Cart.objects.get(cart_id=request.session.session_key).delete()
    except:
        pass

    # Deleting sessions
    del request.session['full_name']
    del request.session['phone']
    del request.session['email']
    del request.session['house_no']
    del request.session['area']
    del request.session['landmark']
    del request.session['town']
    del request.session['state']
    del request.session['pin']
    del request.session['total_price']
    del request.session['tax']
    del request.session['grand_total']
    del request.session['payment_id']


