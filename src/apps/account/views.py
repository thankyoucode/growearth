from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .._utils.message import MessageService

# Import your custom forms
from .forms import (
    UserLoginForm,
    UserRegistrationForm,
)
from .tokens import account_activation_token


def direct_register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            MessageService.success(request, f"New account created: {user.first_name}")
            return redirect("account:login")
        else:
            for error in list(form.errors.values()):
                MessageService.error(request, error)
    form = UserRegistrationForm()
    return render(request, "account/register.html", {"form": form})


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
    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    logout(request)
    MessageService.success(request, "You have been logged out successfully.")
    return redirect("account:login")


def profile_view(request):
    return render(request, "account/profile.html")


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
        return redirect("/account/login")
    else:
        MessageService.success(
            request,
            "Activation link is invalid!",
        )
    return redirect("/home")


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    mail_body = render_to_string(
        "account/activate_account.html",
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


# def register_view(request):
#     form = UserRegistrationForm(request.POST, request.FILES)
#     if request.method == "POST":
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()

#             activateEmail(request, user, form.cleaned_data.get("email"))
#             return redirect("home")

#         else:
#             # Show error messages
#             for field in form.errors:
#                 MessageService.error(
#                     request, f"{field.capitalize()} - {form.errors[field]}"
#                 )

#     else:
#         return render(request, "account/register.html", {"form": form})


# def login_view(request):
#     form = UserLoginForm(request.POST)
#     if request.method == "POST":
#         if form.is_valid():
#             user = authenticate(request, **form.cleaned_data)

#             if user:
#                 MessageService.success(request, f"Welcome, {user.username}!")
#                 login(request, user)
#                 return redirect("dashboard")
#             else:
#                 MessageService.error(request, "Invalid login credentials")

#     return render(request, "account/login.html", {"form": form})
