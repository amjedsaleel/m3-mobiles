# Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm

# local Django
from .forms import AddressForm, UpdateProfileForm
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
    order_products = OrderProduct.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'userProfile/my-orders.html', {'order_products': order_products})


@login_required
def cancel_order_product(request, pk):

    if request.method == 'POST':
        product = OrderProduct.objects.get(pk=pk)
        product.status = 'Canceled'
        product.save()
        return JsonResponse({'message': 'success'})


@login_required
def edit_profile(request):
    form = UpdateProfileForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully profile updated')
            return redirect('userProfile:dashboard')

    return render(request, 'userProfile/edit-profile.html', {'form': form})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated.')
            return redirect('accounts:sign-in')

    return render(request, 'userProfile/change-password.html', {'form': form})

