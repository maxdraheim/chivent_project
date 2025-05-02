from decimal import Decimal
from django.conf import settings
from events.models import Event # Import the Event model from the 'events' app

class Cart:
    """
    Manages the shopping cart stored in the session.
    """
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session if none exists
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, event, quantity=1, update_quantity=False):
        """
        Add an event to the cart or update its quantity.
        Since we are likely only allowing 1 ticket per event type per cart,
        we might simplify this later, but let's keep quantity for now.
        """
        event_id = str(event.id) # Use string for session keys (JSON serializable)

        if event_id not in self.cart:
            self.cart[event_id] = {'quantity': 0, 'price': str(event.price)} # Store price too

        if update_quantity:
            self.cart[event_id]['quantity'] = quantity
        else:
            # For ticketing, usually add means add *one* instance, or maybe replace.
            # Let's assume adding means setting quantity to 1 if not present,
            # or ensuring it stays 1 if already present (no multiple tickets of same type).
            # If you wanted multiple tickets, you'd increment:
            # self.cart[event_id]['quantity'] += quantity
            self.cart[event_id]['quantity'] = 1 # Set/ensure quantity is 1

        # Prevent adding more than 1 ticket per event type if that's the rule
        if self.cart[event_id]['quantity'] > 1:
             self.cart[event_id]['quantity'] = 1

        self.save()

    def save(self):
        """
        Mark the session as "modified" to make sure it gets saved.
        """
        self.session.modified = True

    def remove(self, event):
        """
        Remove an event from the cart.
        """
        event_id = str(event.id)
        if event_id in self.cart:
            del self.cart[event_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the events
        from the database.
        """
        event_ids = self.cart.keys()
        # Get the event objects and add them to the cart
        events = Event.objects.filter(id__in=event_ids)

        cart = self.cart.copy() # Create a copy to modify while iterating
        for event in events:
            cart[str(event.id)]['event'] = event # Add the actual Event object

        for item in cart.values():
            item['price'] = Decimal(item['price']) # Convert price back to Decimal
            item['total_price'] = item['price'] * item['quantity']
            yield item # Yield the dictionary for each item

    def __len__(self):
        """
        Count all items in the cart (sum of quantities).
        For ticketing where quantity is always 1 per event type, this is just the number of event types.
        """
        # return sum(item['quantity'] for item in self.cart.values())
        return len(self.cart.keys()) # Number of different events in cart

    def get_total_price(self):
        """
        Calculate the total cost of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()