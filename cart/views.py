from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST # Ensures a view only accepts POST requests
from events.models import Event # Need the Event model to fetch events
from .cart import Cart # Import the Cart class we created

# Create your views here.

@require_POST # Decorator to ensure only POST requests reach this view
def cart_add(request, event_id):
    """
    View to add an event to the cart.
    """
    cart = Cart(request) # Get the current cart
    event = get_object_or_404(Event, id=event_id) # Get the event object

    # For simplicity, we ignore quantity from the form for now and always add 1
    # quantity = request.POST.get('quantity', 1) # Example if you had quantity input

    cart.add(event=event, quantity=1) # Add the event (Cart class handles quantity logic)

    # Redirect to the cart detail page after adding
    return redirect('cart:cart_detail')


@require_POST # Make removal a POST request for consistency/safety
def cart_remove(request, event_id):
    """
    View to remove an event from the cart.
    """
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)
    cart.remove(event)
    return redirect('cart:cart_detail') # Redirect back to the cart page


def cart_detail(request):
    """
    View to display the cart contents.
    """
    cart = Cart(request) # The context processor already makes 'cart' available,
                         # but getting it here is fine too if needed for other logic.
                         # The template will primarily use the one from the context processor.
    return render(request, 'cart.html') # Context processor handles passing 'cart'