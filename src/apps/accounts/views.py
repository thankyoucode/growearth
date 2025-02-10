from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from .._services.two_factor import EmailVerificationService
from .._utils.message import MessageService

# Import your custom forms
from .forms import (
    UserLoginForm,
    UserRegistrationForm,
)

User = get_user_model()


# Utility Functions
# ! it is not using any where
# TODO if it not use any where try to backup in another util file and delete from here
def render_message(request, template_name, message=None):
    if message:
        messages.error(request, message, extra_tags="alert-danger")
    return render(request, template_name)


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Success message using new service
            MessageService.success(
                request, "Registration successful! Please verify your email."
            )

            # Send verification code
            code = EmailVerificationService.generate_verification_code(user.id)
            EmailVerificationService.send_verification_email(user, code)

            return redirect("verify_email")

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)

            if user:
                MessageService.success(request, f"Welcome back, {user.username}!")
                login(request, user)
                return redirect("dashboard")
            else:
                MessageService.error(request, "Invalid login credentials")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(
        request, "You have been logged out successfully.", extra_tags="alert-success"
    )
    return redirect("login")
