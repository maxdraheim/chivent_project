from django.shortcuts import render, get_object_or_404
from .models import Event

# Create your views here.
def event_catalog(request):
    '''displays the list of upcoming events'''
    events = Event.objects.all()

    context = {
        'events': events,
    }
    return render(request, 'events/catalog.html', context)

def event_detail(request, event_id):
    '''displays the details for a single event.'''

    event = get_object_or_404(Event, pk=event_id)

    context = {
        'event': event,
    }

    return render(request, 'events/event_detail.html', context)