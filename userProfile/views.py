# Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# local Django
from .forms import AddressForm
from .models import Address

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
            messages.success(request, 'Successfully new message added')
            return redirect('userProfile:my-addresses')

    context = {
        'form': form,
        'addresses': addresses
    }
    return render(request, 'userProfile/my-addresses.html', context)
