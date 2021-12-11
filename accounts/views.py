# Stated library
import threading

# django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse

# local Django
from .forms import CustomUserCreationForm, ResetPasswordForm
from .verification import send_otp, verify_otp_number
from cart.utils import get_cart_id
from cart.models import Cart, CartItem

User = get_user_model()


# Create your views here.


def signup(request):
    """
    Sign Up
    """
    if request.user.is_authenticated:
        return redirect('store:index')

    form = CustomUserCreationForm(use_required_attribute=False)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, use_required_attribute=False)

        if form.is_valid():
            form.save()
            phone_number = form.cleaned_data['mobile']
            request.session['phone_number'] = phone_number
            t1 = threading.Thread(target=send_otp, args=(phone_number,))  # Sending OTP for verify user account
            t1.start()
            messages.success(request, 'Successfully account created. Now verify your account with OTP')
            return redirect('accounts:verify-account')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def sign_in(request):
    """
    Sign in with email and password
    """
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if not user.is_verified:  # Checking user is verified or not
                request.session['phone_number'] = user.mobile
                t1 = threading.Thread(target=send_otp, args=(user.mobile,))
                t1.start()
                messages.warning(request, 'Your account is not verified. Verify account with OTP')
                return redirect('accounts:verify-account')

            try:
                cart = Cart.objects.get(cart_id=get_cart_id(request))  # Guest user cart
                is_cart_items = CartItem.objects.filter(
                    cart_id=cart).exists()  # Checking  guest user have any cart items

                if is_cart_items:
                    cart_items = CartItem.objects.filter(cart=cart)

                    for cart_item in cart_items:
                        try:
                            cart_item.user = user
                            cart_item.save()
                        except IntegrityError:
                            user_cart_item = CartItem.objects.get(user=user, variant=cart_item.variant)
                            user_cart_item.quantity += cart_item.quantity
                            user_cart_item.save()
                            cart_item.delete()

            except Cart.DoesNotExist:
                pass
            login(request, user)
            messages.success(request, 'Successfully logged In')

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            return redirect('store:index')
        messages.error(request, 'Invalid credentials')
        return redirect('accounts:sign-in')

    return render(request, 'accounts/sign-in.html')


def log_out(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('store:index')


def verify_account(request):
    """
    Verifying the user account and updating is_verified filed
    """
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        try:
            phone_number = request.session['phone_number']
        except KeyError:
            messages.info(request, 'Session timeout')
            return redirect('accounts:sign-in')

        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)

        if verified:
            user = User.objects.get(mobile=phone_number)
            user.is_verified = True
            user.save()

            try:
                cart = Cart.objects.get(cart_id=get_cart_id(request))  # Guest user cart
                is_cart_items = CartItem.objects.filter(
                    cart_id=cart).exists()  # Checking  guest user have any cart items

                if is_cart_items:
                    cart_items = CartItem.objects.filter(cart=cart)

                    for cart_item in cart_items:
                        try:
                            cart_item.user = user
                            cart_item.save()
                        except IntegrityError:
                            user_cart_item = CartItem.objects.get(user=user, variant=cart_item.variant)
                            user_cart_item.quantity += cart_item.quantity
                            user_cart_item.save()
                            cart_item.delete()

            except Cart.DoesNotExist:
                pass

            login(request, user)
            messages.success(request, 'Successfully account verified')
            return redirect('store:index')
        else:
            messages.error(request, 'Invalid OTP, please try again')
            return redirect('accounts:verify-account')

    return render(request, 'accounts/verify-otp.html')


def mobile_login(request):
    """
    Login with mobile number
    """
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        phone_number = request.POST.get('number')
        try:
            User.objects.get(mobile=phone_number)
            request.session['phone_number'] = phone_number
            t1 = threading.Thread(target=send_otp, args=(phone_number,))
            t1.start()
            messages.success(request, 'OTP sent your mobile number')
            return redirect('accounts:mobile-login-otp-verify')

        except ObjectDoesNotExist:
            messages.error(request, 'Enter a registered mobile number')
            return redirect('accounts:sign-in')


def mobile_login_otp_verify(request):
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        try:
            phone_number = request.session['phone_number']
        except KeyError:
            messages.info(request, 'Session timeout')
            return redirect('accounts:sign-in')

        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)

        if verified:
            user = User.objects.get(mobile=phone_number)

            try:
                cart = Cart.objects.get(cart_id=get_cart_id(request))  # Guest user cart
                is_cart_items = CartItem.objects.filter(
                    cart_id=cart).exists()  # Checking  guest user have any cart items

                if is_cart_items:
                    cart_items = CartItem.objects.filter(cart=cart)

                    for cart_item in cart_items:
                        try:
                            cart_item.user = user
                            cart_item.save()
                        except IntegrityError:
                            user_cart_item = CartItem.objects.get(user=user, variant=cart_item.variant)
                            user_cart_item.quantity += cart_item.quantity
                            user_cart_item.save()
                            cart_item.delete()

            except Cart.DoesNotExist:
                pass

            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('store:index')

        messages.error(request, 'Invalid OTP')
        return redirect('accounts:mobile-login-otp-verify')
    return render(request, 'accounts/verify-otp.html')


def reset_password(request):
    """
    Send OTP to user reset password
    """
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        phone_number = request.POST.get('number')

        try:
            User.objects.get(mobile=phone_number)
            request.session['phone_number'] = phone_number
            t1 = threading.Thread(target=send_otp, args=(phone_number,))
            t1.start()
            return redirect('accounts:verify-reset-password-otp')
        except ObjectDoesNotExist:
            messages.error(request, 'Enter a registered phone number')
            return redirect('accounts:verify-reset-password-otp')

    return render(request, 'accounts/reset-password-otp.html')


def verify_reset_password_otp(request):
    """
    Verify the OPT sent for reset password
    """
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        try:
            phone_number = request.session['phone_number']
        except KeyError:
            messages.info(request, 'Session timeout')
            return redirect('accounts:sign-in')

        otp = request.POST.get('otp')
        verified = verify_otp_number(phone_number, otp)

        if verified:
            return redirect('accounts:set-new-password')

        messages.error(request, 'Invalid OTP, try again')
        return redirect('accounts:reset-password')
    return render(request, 'accounts/verify-otp.html')


def set_new_password(request):
    """
    Set new password
    """
    if request.user.is_authenticated:
        return redirect('store:index')

    if 'phone_number' not in request.session:
        return redirect('accounts:sign-in')

    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['confirm_password']
            try:
                phone_number = request.session['phone_number']
            except KeyError:
                messages.info(request, 'Session timeout')
                return redirect('accounts:sign-in')

            user = User.objects.get(mobile=phone_number)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password is successfully reset')
            return redirect('accounts:sign-in')

    context = {
        'form': form
    }
    return render(request, 'accounts/new-password.html', context)


def resent_otp(request):
    if request.method == 'POST':
        phone_number = request.session['phone_number']
        send_otp(phone_number)
        return JsonResponse({'message': 'success'})
