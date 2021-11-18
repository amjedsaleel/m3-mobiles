# Django
from django.shortcuts import render, redirect

# local Django
from cart.context_processors import cart_items_count

# Create your views here.


def place_order(request):
    count = cart_items_count(request)
    if count['count'] is None:
        return redirect('store:store')

    if request.method == 'POST':
        print('post')
        print(request.POST)

    return render(request, 'order/place-order.html')
