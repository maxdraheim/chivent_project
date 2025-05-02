from .cart import Cart

def cart(request):
    '''makes the cart object available in the template context'''
    return {'cart': Cart(request)}