# django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

# local Django
from .forms import CustomUserCreationForm
from .verification import send_otp, verify_otp_number

User = get_user_model()

# Create your views here.


def signup(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            phone_number = form.cleaned_data['mobile']
            request.session['phone_number'] = phone_number
            send_otp(phone_number)  # Sending OTP for verify user account
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
            if not user.is_verified:
                request.session['phone_number'] = user.mobile
                send_otp(user.mobile)
                messages.warning(request, 'Your account is not verified. Verify account with OTP')
                return redirect('accounts:verify-account')

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


# def account_verification(request):
#     """
#     Send OTP to user phone for verify user account,
#     """
#
#     if request.method == 'POST':
#         phone_number = request.POST.get('number')
#         request.session['phone_number'] = phone_number
#         send_otp(phone_number)
#         return redirect('accounts:verify-otp')
#     return render(request, 'accounts/phone-number.html')


def verify_account(request):
    """
    Verifying the user account and updating is_verified filed
    """

    if request.method == 'POST':
        phone_number = request.session['phone_number']
        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)

        if verified:
            user = User.objects.get(mobile=phone_number)
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('store:index')
        else:
            messages.error(request, 'Invalid OTP, please try again')
            return redirect('accounts:verify-account')

    return render(request, 'accounts/verify-otp.html')
