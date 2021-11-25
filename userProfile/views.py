# Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# local Django
from .forms import AddressForm
from .models import Address
from order.models import OrderProduct

# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'userProfile/dashboard.html')


@login_required
def my_addresses(request):
    form = AddressForm()
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Successfully new address added')
            return redirect('userProfile:my-addresses')

    context = {
        'form': form,
        'addresses': addresses
    }
    return render(request, 'userProfile/my-addresses.html', context)


@login_required
def edit_address(request, pk):
    address = Address.objects.get(pk=pk)
    form = AddressForm(instance=address)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your address is updated')
            return redirect('userProfile:my-addresses')

    context = {
        'form': form
    }
    return render(request, 'userProfile/edit-address.html', context)


@login_required
def delete_address(request, pk):
    if request.is_ajax():
        Address.objects.get(pk=pk).delete()
        return JsonResponse({'message': 'success'})


@login_required
def set_default_address(request, pk):
    Address.objects.filter(user=request.user, default=True).update(default=False)
    address = Address.objects.get(pk=pk)
    address.default = True
    address.save()
    messages.success(request, 'Default address changed')
    return redirect('userProfile:my-addresses')


@login_required
def my_orders(request):
    order_products = OrderProduct.objects.filter(user=request.user)
    return render(request, 'userProfile/my-orders.html', {'order_products': order_products})
