from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from products.models import Cart
from .models import Order, OrderItem, Payment
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=request.POST.get('shipping_address'),
            billing_address=request.POST.get('billing_address'),
            phone_number=request.POST.get('phone_number'),
            subtotal=cart.total_price,
            total=cart.total_price,
        )
        
        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_discounted_price()
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return redirect('orders:payment', order_id=order.order_id)
    
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),  # Convert to cents
                currency='usd',
                metadata={'order_id': order.order_id}
            )
            
            order.payment_id = intent.id
            order.payment_status = 'paid'
            order.status = 'processing'
            order.save()
            
            # Update user profile stats
            request.user.userprofile.update_purchase_stats(order.total)
            
            return redirect('orders:payment_success', order_id=order.order_id)
            
        except stripe.error.CardError as e:
            messages.error(request, f'Payment failed: {e.user_message}')
        except Exception as e:
            messages.error(request, 'Payment processing error occurred.')
    
    return render(request, 'orders/payment.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/payment_success.html', {'order': order})

def payment_cancel(request):
    return render(request, 'orders/payment_cancel.html')