# Django
from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma

# local Django
from .models import Order
from .forms import OrderForm
from cart.context_processors import cart_items_count
from cart.utils import cart_summery, get_cart_items

# Create your views here.


def place_order(request):
    count = cart_items_count(request)
    if count['count'] is None:
        return redirect('store:store')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = cart_summery(request)
            order = form.save(commit=False)
            order.order_total = int(data['total_price'])
            order.tax = int(data['tax'])
            order.grand_total = int(data['grand_total'])
            order.user = request.user
            order.save()
            request.session['order_id'] = order.id
            return redirect('order:review-order')
        return redirect('order:place-order')


def review_order(request):
    cart_items = get_cart_items(request)
    result = cart_summery(request)  # Get cart summery with total price, tax, grand total
    order = Order.objects.get(pk=request.session['order_id'])

    context = {
        'cart_items': cart_items,
        'tax': intcomma(result['tax']),
        'total': intcomma(result['total_price']),
        'grand_total': intcomma(result['grand_total']),
        'order': order
    }
    return render(request, 'order/review-order.html', context)
