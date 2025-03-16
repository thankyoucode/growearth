from pathlib import Path
from pyexpat.errors import messages

from django.conf import settings

# from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from dotenv import load_dotenv

from .._utils.message import MessageService
from ..store.models import Order

# Import your custom forms
from .forms import (
    ChangePasswordForm,
    EditProfileForm,
    UserLoginForm,
    UserOpinionForm,
    UserRegistrationForm,
)
from .models import UserOpinion
from .tokens import account_activation_token

# Core Project Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv()


def direct_register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            MessageService.success(request, f"New account created: {user.first_name}")
            return redirect("accounts:login")
        else:
            for error in list(form.errors.values()):
                MessageService.error(request, error)
    form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def direct_login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                MessageService.success(request, f"Welcome, {user.first_name}!")
                login(request, user)
                return redirect("core:home")
        else:
            MessageService.error(
                request,
                "Invalid login credentials, please enter valid email and password",
            )
    form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    MessageService.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")


@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    orders = user.orders.all()  # Fetch all orders related to the user

    context = {
        "user": user,
        "orders": orders,  # Pass orders to the template
    }
    return render(request, "accounts/profile.html", context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        MessageService.success(
            request,
            "Thank you for your email confirmation, Now you can login your account.",
        )
        return redirect("/accounts/login")
    else:
        MessageService.success(
            request,
            "Activation link is invalid!",
        )
    return redirect("/home")


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    mail_body = render_to_string(
        "accounts/activate_account.html",
        {
            "user": user.first_name,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(
        subject=mail_subject,
        body=mail_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[to_email],
    )
    if email.send():
        MessageService.success(
            request,
            f"Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.",
        )
    else:
        MessageService.error(
            request,
            f"Problem sending email to {to_email}, check if you typed it currectly.",
        )


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, instance=request.user)
        password_form = ChangePasswordForm(request.user, request.POST)

        if profile_form.is_valid():
            profile_form.save()
            MessageService.success(
                request, "Your profile has been updated successfully!"
            )
            return redirect("accounts:profile")

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            MessageService.success(
                request, "Your password has been updated successfully!"
            )
            return redirect("accounts:profile")
        else:
            for error in list(password_form.errors.values()):
                MessageService.error(
                    request, error[0]
                )  # Display each password form error

            MessageService.error(request, "Please correct the errors below.")

    else:
        profile_form = EditProfileForm(instance=request.user)
        password_form = ChangePasswordForm(request.user)

    context = {
        "profile_form": profile_form,
        "password_form": password_form,
    }
    return render(request, "accounts/edit_profile.html", context)


@login_required
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # Delete the user account
        MessageService.success(request, "Your account has been deleted successfully.")
        return redirect("home")  # Redirect to home or login page after deletion

    # No GET handling needed since confirmation is done via modal


@login_required
def submit_opinion(request):
    if request.method == "POST":
        form = UserOpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.user = request.user
            # If no rating is provided, set it to None
            if not request.POST.get("rating"):
                opinion.rating = None
            else:
                opinion.rating = request.POST.get("rating")
            opinion.save()

            return redirect("accounts:review_list")
        else:
            return render(
                request,
                "accounts:review_list",
                {"form": form, "reviews": UserOpinion.objects.filter(is_review=True)},
            )
    else:
        return redirect("accounts:review_list")


def review_list(request):
    reviews = UserOpinion.objects.filter(is_review=True)
    form = UserOpinionForm()
    for review in reviews:
        review.star_list = range(
            review.rating
        )  # Generate a list of stars based on the rating
    return render(request, "accounts/review.html", {"reviews": reviews, "form": form})
