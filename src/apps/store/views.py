from django.shortcuts import render
from django.views.generic import View

from .forms import ManageCategoryForm
from .models import Category, Plant


class ManageCategoryView(View):
    def get(self, request):
        form = ManageCategoryForm()
        return render(request, "store/manage_category.html", {"form": form})

    def post(self, request):
        form = ManageCategoryForm(request.POST)

        if form.is_valid():
            form.save()


def plants_view(request):
    # plants = Plant.objects.all().order_by("created_at")
    plants = Plant.objects.all()
    categoryes = Category.objects.all()
    return render(
        request, "store/plants.html", {"plants": plants, "categoryes": categoryes}
    )


def collections_view(request):
    return render(request, "store/collections.html")


def care_guide_view(request):
    return render(request, "store/care_guide.html")


def catalog_view(request):
    return render(request, "store/catalog.html")
