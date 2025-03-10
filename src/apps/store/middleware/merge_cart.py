import uuid

from ..models import CartItem, Plant


class MergeCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and "cart" in request.session:
            # Merge session-based cart with user-connected cart
            session_cart = request.session.get("cart", {})
            for plant_id_str, quantity in session_cart.items():
                try:
                    plant_id = uuid.UUID(plant_id_str)
                    plant = Plant.objects.get(id=plant_id)

                    # Check if item already exists in user's cart
                    cart_item, created = CartItem.objects.get_or_create(
                        user=request.user, plant=plant, defaults={"quantity": quantity}
                    )
                    if not created:
                        # Update quantity if item already exists
                        cart_item.quantity += quantity
                        cart_item.save()
                except (Plant.DoesNotExist, ValueError):
                    pass  # Skip invalid or non-existent plants

            # Clear session-based cart after merging
            del request.session["cart"]
            request.session.modified = True

        response = self.get_response(request)
        return response
