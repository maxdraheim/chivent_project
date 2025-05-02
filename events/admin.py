from django.contrib import admin
from .models import Event
# Register your models here.
@admin.register(Event)

class EventAdmin(admin.ModelAdmin):
    '''Costomizes the appearance and behavior of the Event model in the admin site.'''

    '''columns shown in list view'''
    list_display = ('title', 'location', 'start_datetime', 'price', 'id')

    '''fields to filter byin the sidebar'''
    list_filter = ('start_datetime', 'location')

    '''Fields in the search bar'''
    search_fields = ('title', 'description', 'location')

    '''adds date drill down navigation'''
    date_hierarchy = 'start_datetime'
    ordering = ('start_datetime',)