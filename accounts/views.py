# django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# local Django
from .forms import CustomUserCreationForm

# Create your views here.


def signup(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:signup')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def sign_in(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:index')

        messages.error(request, 'Invalid credentials')
        return redirect('accounts:sign-in')

    return render(request, 'accounts/sign-in.html')
