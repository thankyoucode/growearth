import uuid
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from apps._utils.message import MessageService

from .forms import (
    CheckoutForm,  # Assuming you have a CheckoutForm  # Assuming you have a CheckoutForm
    ManageCategoryForm,
)
from .models import (  # Assuming you have these models  # Make sure to import OrderItem
    CartItem,
    Category,
    Order,
    OrderItem,
    Plant,
)  # Assuming Order and OrderItem models


class ManageCategoryView(View):
    def get(self, request):
        form = ManageCategoryForm()
        return render(request, "store/manage_category.html", {"form": form})

    def post(self, request):
        form = ManageCategoryForm(request.POST)

        if form.is_valid():
            form.save()


def categoryes_view(request):
    categoryes = Category.objects.all()
    return render(request, "store/categoryes.html", {"categoryes": categoryes})


# it get all plants from that category
def category_plants_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    plants = Plant.objects.filter(category=category)
    return render(
        request, "store/category_plants.html", {"category": category, "plants": plants}
    )


# it get send plant get by that id
def plant_view(request, id):
    plant = get_object_or_404(Plant, id=id)
    return render(request, "store/plant_details.html", {"plant": plant})


SHIPPING_COST: float = 50


def cart_view(request):
    if request.user.is_authenticated:
        # Fetch authenticated user's cart items
        cart_items = CartItem.objects.filter(user=request.user).select_related("plant")
        subtotal = sum(item.plant.price * item.quantity for item in cart_items)
        total = subtotal + SHIPPING_COST  # Example shipping cost
    else:
        # Fetch guest user's session-based cart items
        session_cart = request.session.get("cart", {})
        cart_items = []
        subtotal = 0

        for plant_id_str, quantity in session_cart.items():
            try:
                plant_id = uuid.UUID(plant_id_str)
                plant = Plant.objects.get(id=plant_id)
                total_price = plant.price * quantity
                cart_items.append(
                    {
                        "plant": plant,
                        "quantity": quantity,
                        "total_price": total_price,
                    }
                )
                subtotal += total_price
            except (Plant.DoesNotExist, ValueError):
                pass  # Skip invalid or non-existent plants

        total = subtotal + SHIPPING_COST  # Example

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": total,
    }
    return render(request, "store/cart.html", context)


@csrf_exempt
def add_to_cart_view(request, plant_id):
    try:
        # Validate UUID format and fetch the plant object
        plant_id = uuid.UUID(str(plant_id))
        plant = get_object_or_404(Plant, id=plant_id)
    except ValueError:
        MessageService.error(request, "Invalid plant ID format.")
        return JsonResponse(
            {"success": False, "message": "Invalid plant ID format."}, status=400
        )
    except Plant.DoesNotExist:
        MessageService.error(request, "Plant not found.")
        return JsonResponse(
            {"success": False, "message": "Plant not found."}, status=404
        )

    if request.user.is_authenticated:
        # Handle authenticated user's cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, plant=plant, defaults={"quantity": 1}
        )
        if created:
            if plant.inventory < 1:
                cart_item.delete()
                MessageService.error(request, f"{plant.title} is out of stock.")
                return JsonResponse(
                    {"success": False, "message": f"{plant.title} is out of stock."},
                    status=400,
                )
            print(f"Created new cart item for {plant.title}")  # Debugging log
            message = f"{plant.title} added to your cart successfully!"
            MessageService.success(request, message)
        else:
            if cart_item.quantity + 1 > plant.inventory:
                MessageService.error(
                    request,
                    f"Cannot add more {plant.title}. Only {plant.inventory} left in stock.",
                )
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Cannot add more {plant.title}. Only {plant.inventory} left in stock.",
                    },
                    status=400,
                )
            print(f"Updated quantity for {plant.title}")  # Debugging log
            cart_item.quantity += 1
            cart_item.save()
            message = f"{plant.title} quantity updated in your cart."
            MessageService.info(request, message)
    else:
        # Handle guest user's cart using session
        cart = request.session.get("cart", {})
        plant_id_str = str(plant_id)

        if plant_id_str in cart:
            if cart[plant_id_str] + 1 > plant.inventory:
                MessageService.error(
                    request,
                    f"Cannot add more {plant.title}. Only {plant.inventory} left in stock.",
                )
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Cannot add more {plant.title}. Only {plant.inventory} left in stock.",
                    },
                    status=400,
                )
            print(f"Updated quantity for guest cart: {plant.title}")  # Debugging log
            cart[plant_id_str] += 1
            message = f"{plant.title} quantity updated in your guest cart."
            MessageService.info(request, message)
        else:
            if plant.inventory < 1:
                MessageService.error(request, f"{plant.title} is out of stock.")
                return JsonResponse(
                    {"success": False, "message": f"{plant.title} is out of stock."},
                    status=400,
                )
            print(f"Added new item to guest cart: {plant.title}")  # Debugging log
            cart[plant_id_str] = 1
            message = f"{plant.title} added to your guest cart successfully!"
            MessageService.success(request, message)

        request.session["cart"] = cart
        request.session.modified = True  # Mark session as modified

    return JsonResponse({"success": True, "message": message}, status=200)


@csrf_exempt
def update_cart_view(request, plant_id):
    try:
        plant_id = uuid.UUID(str(plant_id))
        plant = get_object_or_404(Plant, id=plant_id)
    except (ValueError, Plant.DoesNotExist):
        MessageService.error(request, "Invalid plant ID or plant not found.")
        return JsonResponse(
            {"success": False, "message": "Invalid plant ID or plant not found."},
            status=400,
        )

    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))

            if quantity < 1:
                MessageService.warning(request, "Quantity must be at least 1.")
                return JsonResponse(
                    {"success": False, "message": "Quantity must be at least 1."},
                    status=400,
                )

            if quantity > plant.inventory:
                msg = f"Only {plant.inventory} {plant.title} available."
                MessageService.error(request, msg)

            elif request.user.is_authenticated:
                cart_item, created = CartItem.objects.get_or_create(
                    user=request.user, plant=plant, defaults={"quantity": 0}
                )
                cart_item.quantity = quantity
                cart_item.save()
                MessageService.success(
                    request,
                    f"Updated {plant.title} quantity to {quantity} in your cart.",
                )

            else:
                cart = request.session.get("cart", {})
                cart[str(plant_id)] = quantity
                request.session["cart"] = cart
                request.session.modified = True
                MessageService.success(
                    request,
                    f"Updated {plant.title} quantity to {quantity} in your guest cart.",
                )

            return JsonResponse({"success": True})

        except ValueError:
            MessageService.error(request, "Invalid quantity.")

    MessageService.error(request, "Invalid request method.")


@csrf_exempt
def remove_from_cart_view(request, plant_id):
    try:
        # Validate UUID format
        plant_id = uuid.UUID(str(plant_id))
        plant = get_object_or_404(Plant, id=plant_id)
    except (ValueError, Plant.DoesNotExist):
        MessageService.error(request, "Invalid plant ID or plant not found.")
        return JsonResponse(
            {"success": False, "message": "Invalid plant ID or plant not found."},
            status=400,
        )

    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(user=request.user, plant=plant)
                cart_item.delete()
                MessageService.success(
                    request,
                    f"{plant.title} removed from your authenticated user cart.",
                )
            except CartItem.DoesNotExist:
                MessageService.error(
                    request, "Item not in your authenticated user cart."
                )
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Item not in your authenticated user cart.",
                    },
                    status=404,
                )
        else:
            # Handle session-based cart for unauthenticated users
            cart = request.session.get("cart", {})
            plant_id_str = str(plant_id)
            if plant_id_str not in cart:
                MessageService.error(request, "Item not in your guest user cart.")
                return JsonResponse(
                    {"success": False, "message": "Item not in your guest user cart."},
                    status=404,
                )
            del cart[plant_id_str]
            request.session["cart"] = cart
            request.session.modified = True

            MessageService.success(
                request,
                f"{plant.title} removed from your guest user cart.",
            )

        return JsonResponse({"success": True})

    MessageService.error(request, "Invalid request method.")
    return JsonResponse(
        {"success": False, "message": "Invalid request method."}, status=400
    )


@login_required
def checkout_view(request):
    # Fetch authenticated user's cart items
    cart_items = CartItem.objects.filter(user=request.user).select_related("plant")
    processed_cart_items = []
    total_price = Decimal(0)

    # Validate inventory and calculate total price
    for item in cart_items:
        if item.quantity > item.plant.inventory:
            MessageService.error(
                request,
                f"Insufficient stock for {item.plant.title}. Only {item.plant.inventory} left in stock.",
            )
            return redirect(
                "store:cart"
            )  # Redirect back to the cart page if validation fails

        item_total = item.plant.price * Decimal(item.quantity)
        total_price += item_total
        processed_cart_items.append(
            {
                "plant": item.plant,
                "quantity": item.quantity,
                "total_price": item_total,
            }
        )

    # Initialize shipping cost (default value)
    shipping_cost = Decimal(50.00)  # Example shipping cost

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            shipping_address = form.cleaned_data["shipping_address"]
            billing_address = form.cleaned_data["billing_address"]
            payment_method = form.cleaned_data["payment_method"]

            # Create an order
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                billing_address=billing_address,
                payment_method=payment_method,
                total_price=total_price + shipping_cost,
                status="PENDING",
                payment_status="PENDING",
            )

            # Create OrderItems for each cart item and reduce inventory
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    plant=item.plant,
                    quantity=item.quantity,
                    price=item.plant.price,  # Use current price from Plant model
                )

                # Reduce inventory for each ordered item
                item.plant.inventory -= item.quantity
                item.plant.save()

            # Clear authenticated user's cart after placing the order
            CartItem.objects.filter(user=request.user).delete()

            # Redirect to order confirmation page
            MessageService.success(request, "Order placed successfully!")
            return redirect("store:order_confirmation", order_id=order.id)

    else:
        form = CheckoutForm()

    return render(
        request,
        "store/checkout.html",
        {
            "form": form,
            "cart_items": processed_cart_items,
            "subtotal": total_price,
            "shipping_cost": shipping_cost,
            "total": total_price + shipping_cost,
        },
    )


@login_required
def order_confirmation_view(request, order_id):
    """
    Display the order confirmation page for a specific order.
    Ensure the order belongs to the logged-in user.
    """
    # Fetch the order and verify it belongs to the logged-in user
    try:
        order = get_object_or_404(Order, id=order_id)
        if order.user != request.user:
            return HttpResponseForbidden("You are not authorized to view this order.")
    except Order.DoesNotExist:
        return render(request, "store/error.html", {"message": "Order not found."})

    # Prepare context for the template
    context = {
        "order": order,
        "order_items": order.items.all(),  # Assuming related_name="items" in OrderItem model
    }

    return render(request, "store/order_confirmation.html", context)
