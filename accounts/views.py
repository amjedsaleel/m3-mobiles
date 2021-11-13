# django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# local Django
from .forms import CustomUserCreationForm
from .verification import send_otp, verify_otp_number

# Create your views here.


def signup(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:verify-account')

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
            messages.success(request, 'Successfully logged In')
            return redirect('store:index')

        messages.error(request, 'Invalid credentials')
        return redirect('accounts:sign-in')

    return render(request, 'accounts/sign-in.html')


def log_out(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('store:index')


def verify_account(request):

    if request.method == 'POST':
        phone_number = request.POST.get('number')
        request.session['phone_number'] = phone_number
        send_otp(phone_number)
        return redirect('accounts:verify-otp')
    return render(request, 'accounts/phone-number.html')


def verity_opt(request):

    if request.method == 'POST':
        phone_number = request.session['phone_number']
        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)

        if verified:
            print("Success")
        else:
            print("Error")

    return render(request, 'accounts/verify-otp.html')
