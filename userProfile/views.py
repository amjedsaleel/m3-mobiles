from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'userProfile/dashboard.html')