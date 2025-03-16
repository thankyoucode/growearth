# views.py
from django.db.models import Q

# core/views.py
from django.shortcuts import render

from apps._utils.message import MessageService

from .decorators import admin_required
from .forms import ContactForm
from .models import Contact  # Assuming you have this model defined


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)


def home_view(request):
    return render(request, "core/home.html")


def impact_view(request):
    return render(request, "core/impact.html")


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_data = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "country": form.cleaned_data["country"],
                "phone": form.cleaned_data["phone"],
                "message": form.cleaned_data["message"],
            }

            contact = Contact(**contact_data)
            contact.save()
            MessageService.success(request, "Message successfully sent!")
        else:
            MessageService.success(request, form.errors)
    else:
        form = ContactForm()
        return render(request, "core/contact.html", {"form": form})


def care_guide_view(request):
    return render(request, "core/care_guide.html")


@admin_required
def contact_messages_view(request):
    query = request.GET.get("q")  # Get the search query from the request
    if query:
        # Filter messages by name or email
        contact_messages = Contact.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        ).order_by("-id")
    else:
        contact_messages = Contact.objects.all().order_by(
            "-id"
        )  # Fetch all messages if no query

    return render(
        request, "core/contact_messages.html", {"contact_messages": contact_messages}
    )


def mission_view(request):
    return render(request, "core/mission.html")


def shipping_view(request):
    return render(request, "core/shipping.html")


def returns_view(request):
    return render(request, "core/returns.html")


def termsofservice_view(request):
    return render(request, "core/termsofservice.html")


def faq_view(request):
    return render(request, "core/faq.html")
