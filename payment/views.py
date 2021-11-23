# third party
import razorpay

# Django
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

# local Django
from .models import Payment
from order.utils import make_order

# Create your views here.

client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def paypal(request):
    if request.is_ajax():
        transaction_id = request.POST.get('transactionId')

        # Saving payment details
        payment = Payment.objects.create(
            user=request.user,
            payment_id=transaction_id,
            amount_paid=request.session['grand_total'],
            payment_method='PayPal',
            status=True
        )
        payment.save()
        request.session['payment_id'] = payment.id
        make_order(request)
        return JsonResponse({'message': 'success'})


def razorpay_payment_verification(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
        except:
            return JsonResponse({'messages': 'error'})

        # Saving payment details
        payment = Payment.objects.create(
            user=request.user,
            payment_id=razorpay_payment_id,
            amount_paid=request.session['grand_total'],
            payment_method='razorpay',
            status=True
        )
        request.session['payment_id'] = payment.id
        make_order(request)

        return JsonResponse({'message': 'success'})
