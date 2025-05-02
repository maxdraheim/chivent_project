# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from events.models import Event
from .cart import Cart

@require_POST
def cart_add(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)

    # Get quantity from POST data, default to 1 if not found or invalid
    try:
        quantity_str = request.POST.get('quantity', '1')
        quantity = int(quantity_str)
        if quantity < 1: # Ensure quantity is at least 1 when adding
            quantity = 1

    except ValueError:
        quantity = 1 # Default to 1 if conversion fails

    cart.add(event=event, quantity=quantity)

    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)
    cart.remove(event)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart}) 