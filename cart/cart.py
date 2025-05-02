# cart/cart.py
from decimal import Decimal
from django.conf import settings
from events.models import Event

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, event, quantity=1, update_quantity=False):
        """
        Add an event to the cart or update its quantity.
        """
        event_id = str(event.id)
        price = str(event.price) # Store price as string in session

        # If the event is not in the cart, initialize its entry
        if event_id not in self.cart:
            self.cart[event_id] = {'quantity': 0, 'price': price}

        # If update_quantity is True, set the quantity directly
        if update_quantity:
            self.cart[event_id]['quantity'] = quantity
        else:
            # Otherwise, increment the quantity by the amount added
            self.cart[event_id]['quantity'] += quantity

        # Ensure quantity doesn't go below zero if update_quantity allows it (optional safeguard)
        if self.cart[event_id]['quantity'] <= 0:
             self.remove(event) # Remove item if quantity becomes zero or less
        else:
             self.save() # Save changes only if item remains

    def save(self):
        self.session.modified = True

    def remove(self, event):
        """
        Remove an event entirely from the cart.
        """
        event_id = str(event.id)
        if event_id in self.cart:
            del self.cart[event_id]
            self.save()

    def __iter__(self):
        event_ids = self.cart.keys()
        events = Event.objects.filter(id__in=event_ids)

        cart = self.cart.copy()
        for event in events:
            cart[str(event.id)]['event'] = event

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            # Calculate total price for this item line
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count the total number of tickets (sum of quantities) in the cart.
        """
        # Sum the quantity for each item in the cart dictionary
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()