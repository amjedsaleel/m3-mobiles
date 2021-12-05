# third-party
from forex_python.converter import CurrencyRates
import razorpay

# Django
from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.conf import settings

# local Django
from .forms import OrderForm
from cart.context_processors import cart_items_count
from cart.utils import get_cart_items
from store.models import Variant

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
def buy_now_place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            request.session['full_name'] = form.cleaned_data['full_name']
            request.session['phone'] = form.cleaned_data['phone']
            request.session['email'] = form.cleaned_data['email']
            request.session['house_no'] = form.cleaned_data['house_no']
            request.session['area'] = form.cleaned_data['area']
            request.session['landmark'] = form.cleaned_data['landmark']
            request.session['town'] = form.cleaned_data['town']
            request.session['state'] = form.cleaned_data['state']
            request.session['pin'] = form.cleaned_data['pin']
            return redirect(f'/order/buy-now/review-order/?variant={request.POST.get("variant")}')
        return redirect('order:buy-now-place-order')


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
def buy_now_review_order(request):
    try:
        variant = Variant.objects.get(slug=request.GET.get('variant'))
    except Variant.DoesNotExist:
        return redirect('store:store')

    rate = dollar_rate()
    total = variant.mrp
    tax = variant.tax
    grand_total = total + tax

    pay_pal_amount = round(grand_total / rate, 2)

    razor_pay_amount = grand_total * 100
    data = {"amount": razor_pay_amount, "currency": "INR"}
    payment = client.order.create(data=data)

    context = {
        'tax': intcomma(tax),
        'total': intcomma(total),
        'grand_total': intcomma(grand_total),
        'pay_pal_amount': pay_pal_amount,
        'razor_key': settings.RAZOR_KEY_ID,
        'order_id': payment['id'],
        'razor_pay_amount': razor_pay_amount,
        'variant': variant
    }

    return render(request, 'order/buy-now-review-order.html', context)


@login_required
def order_completed(request):
    return render(request, 'order/order-complete.html')
