from django.shortcuts import render


def plants_view(request):
    return render(request, "store/plants.html")


def collections_view(request):
    return render(request, "store/collections.html")


def care_guide_view(request):
    return render(request, "store/care_guide.html")


def catalog_view(request):
    return render(request, "store/catalog.html")
