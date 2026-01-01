from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    if cart.items.count() == 0:
        return redirect('product_list')

    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price
        )

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart
        cart.items.all().delete()

        return render(request, 'orders/order_success.html', {'order': order})

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})
