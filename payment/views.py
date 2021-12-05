# Stated library
import threading
from datetime import datetime

# third party
import razorpay

# Django
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages

# local Django
from .models import Payment
from accounts.verification import send_otp, verify_otp_number
from order.utils import make_order, buy_now_make_order
from offer.utils import use_coupon
from store.models import Variant


# Create your views here.

client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def paypal(request):
    if request.is_ajax():
        transaction_id = request.POST.get('transactionId')
        buy_now = request.POST.get('buyNow', False)
        use_coupon(request)

        if buy_now:
            variant_slug = request.POST.get('variantSlug')
            variant = Variant.objects.get(slug=variant_slug)
            grand_total = (variant.mrp + variant.tax) - request.session['discount']
            request.session['buy_now_total'] = variant.mrp
            request.session['buy_now_tax'] = variant.tax
            request.session['buy_now_grand_total'] = grand_total
            request.session['buy_now_variant_slug'] = variant_slug
        else:
            grand_total = request.session['grand_total']

        # Saving payment details
        payment = Payment.objects.create(
            user=request.user,
            payment_id=transaction_id,
            amount_paid=grand_total,
            coupon_discount=request.session['discount'],
            payment_method='PayPal',
            status=True
        )
        payment.save()
        request.session['payment_id'] = payment.id

        if buy_now:
            buy_now_make_order(request)
        else:
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

        use_coupon(request)

        # Saving payment details
        payment = Payment.objects.create(
            user=request.user,
            payment_id=razorpay_payment_id,
            coupon_discount=request.session['discount'],
            amount_paid=request.session['grand_total'],
            payment_method='razorpay',
            status=True
        )
        request.session['payment_id'] = payment.id
        make_order(request)

        return JsonResponse({'message': 'success'})


def failed(request):
    return render(request, 'payment/payment-failed.html')


def cod_confirmation(request):
    t1 = threading.Thread(target=send_otp, args=(request.user.mobile, ))
    t1.start()
    messages.success(request, 'Enter otp to complete order')
    return redirect('payments:cash-on-delivery')


def cash_on_delivery(request):

    if request.method == 'POST':
        otp = request.POST.get('otp')
        verify = verify_otp_number(request.user.mobile, otp)

        if verify:
            use_coupon(request)

            # Saving payment details
            payment = Payment.objects.create(
                user=request.user,
                payment_id=f'COD{datetime.now().strftime("%Y%m%d%H%M%S")}',
                coupon_discount=request.session['discount'],
                amount_paid=request.session['grand_total'],
                payment_method='COD',
                status=True
            )
            request.session['payment_id'] = payment.id
            make_order(request)
            return redirect('order:order-completed')

        messages.error(request, 'Invalid OTP')
        return redirect('payments:cash-on-delivery')
    return render(request, 'accounts/verify-otp.html')
