# Django
from django.shortcuts import render, redirect

# local Django
from .forms import OrderForm
from cart.context_processors import cart_items_count
from cart.utils import cart_summery

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
    return render(request, 'order/place-order.html')
