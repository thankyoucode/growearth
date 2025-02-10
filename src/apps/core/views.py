from django.shortcuts import render


def home_view(request):
    return render(request, "core/home.html")


def impact_view(request):
    return render(request, "core/impact.html")


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    return render(request, "core/contact.html")


def mission_view(request):
    return render(request, "core/mission.html")


def shipping_view(request):
    return render(request, "core/shipping.html")


def returns_view(request):
    return render(request, "core/returns.html")


def consultation_view(request):
    return render(request, "core/consultation.html")


def faq_view(request):
    return render(request, "core/faq.html")
