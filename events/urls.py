from django.urls import path
from . import views

urlpatterns = [
    #path for the event catalog (homepage)
    path('', views.event_catalog, name = 'event_catalog'),

    #path for an events homepage where the int is the event_id
    path('event/<int:event_id>/', views.event_detail, name= 'event_detail'),


]

