import uuid

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import CartItem, Plant


@receiver(user_logged_in)
def merge_carts(sender, request, user, **kwargs):
    """
    Merge session-based cart into the authenticated user's cart upon login.
    """
    session_cart = request.session.get("cart", {})
    if not session_cart:
        return  # No session cart to merge

    for plant_id_str, quantity in session_cart.items():
        try:
            plant_id = uuid.UUID(plant_id_str)
            plant = Plant.objects.get(id=plant_id)
            # Merge into authenticated user's cart
            cart_item, created = CartItem.objects.get_or_create(
                user=user, plant=plant, defaults={"quantity": quantity}
            )
            if not created:
                # If the item already exists, update the quantity
                cart_item.quantity += quantity
                cart_item.save()
        except (ValueError, Plant.DoesNotExist):
            continue  # Skip invalid or non-existent plants

    # Clear the session-based cart after merging
    request.session["cart"] = {}
    request.session.modified = True
