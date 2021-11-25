# third-party
from forex_python.converter import CurrencyRates
import razorpay

# Django
from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.conf import settings


# local Django
from .models import Order
from .forms import OrderForm
from cart.context_processors import cart_items_count
from cart.utils import get_cart_items


client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.


def dollar_rate():
    c = CurrencyRates()
    rate = c.get_rate('USD', 'INR')
    return rate


def place_order(request):
    count = cart_items_count(request)
    if count['count'] is None:
        return redirect('store:store')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # order = form.save(commit=False)
            # order.order_total = int(request.session['total_price'])
            # order.tax = int(request.session['tax'])
            # order.grand_total = int(request.session['grand_total'])
            # order.user = request.user
            # order.save()
            # request.session['order_id'] = order.id
            request.session['full_name'] = form.cleaned_data['full_name']
            request.session['phone'] = form.cleaned_data['phone']
            request.session['email'] = form.cleaned_data['email']
            request.session['house_no'] = form.cleaned_data['house_no']
            request.session['area'] = form.cleaned_data['area']
            request.session['landmark'] = form.cleaned_data['landmark']
            request.session['town'] = form.cleaned_data['town']
            request.session['state'] = form.cleaned_data['state']
            request.session['pin'] = form.cleaned_data['pin']
            return redirect('order:review-order')
        return redirect('order:place-order')


@login_required
def review_order(request):

    if 'tax' not in request.session:
        return redirect('store:store')

    cart_items = get_cart_items(request)
    rate = dollar_rate()
    pay_pal_amount = round((request.session['grand_total']) / rate, 2)

    razor_pay_amount = request.session['grand_total'] * 100
    data = {"amount": razor_pay_amount, "currency": "INR"}
    payment = client.order.create(data=data)

    context = {
        'cart_items': cart_items,
        'tax': intcomma(request.session['tax']),
        'total': intcomma(request.session['total_price']),
        'grand_total': intcomma(request.session['grand_total']),
        'pay_pal_amount': pay_pal_amount,
        'razor_key': settings.RAZOR_KEY_ID,
        'order_id': payment['id'],
        'razor_pay_amount': razor_pay_amount
    }
    return render(request, 'order/review-order.html', context)


@login_required
def order_completed(request):
    return render(request, 'order/order-complete.html')
