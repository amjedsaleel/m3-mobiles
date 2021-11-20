# Django
from django.shortcuts import render
from django.http import JsonResponse

# local Django
from wheel.metadata import pkginfo_unicode

from .models import Payment
from order.models import Order, OrderProduct
from cart.models import CartItem, Variant

# Create your views here.


def paypal(request):
    if request.is_ajax():
        order_number = request.POST.get('orderNumber')
        transaction_id = request.POST.get('transactionId')

        try:
            order = Order.objects.get(user=request.user, order_number=order_number, is_ordered=False)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'error'})

        # Saving payment details
        payment = Payment.objects.create(
            user=request.user,
            payment_id=transaction_id,
            amount_paid=order.order_total,
            payment_method='PayPal',
            status=True
        )
        payment.save()

        # Updating order
        order.payment = payment
        order.is_ordered = True
        order.save()

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

        # Deleting all cart items
        cart_items.delete()

        return JsonResponse({'message': 'success'})

