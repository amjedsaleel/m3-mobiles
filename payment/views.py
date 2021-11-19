# Django
from django.shortcuts import render
from django.http import JsonResponse

# local Django
from .models import Payment
from order.models import Order

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

        return JsonResponse({'success': 'success'})

