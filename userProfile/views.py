from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'userProfile/dashboard.html')


def my_addresses(request):
    return render(request, 'userProfile/my-addresses.html')

