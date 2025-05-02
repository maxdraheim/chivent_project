from django.urls import path
from . import views # We'll create these views soon

app_name = 'cart' # Define the namespace used in templates {% url 'cart:...' %}

urlpatterns = [
    #path for viewing the cart detail page
    path('', views.cart_detail, name='cart_detail'),
    #paths for the adding and removing of an item to cart
    path('add/<int:event_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:event_id>/', views.cart_remove, name='cart_remove'),
]