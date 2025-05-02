from django.db import models

# Create your models here.
class Event(models.Model):
    '''this is an event in the system'''
    title = models.CharField(
        max_length=200,
        help_text= "The main title of the event."
    )

    description = models.TextField(
        help_text="A detailed description of the event"
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="a url to an image representing the event (not necessary)"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="The price of a single ticket."
    )
    location = models.CharField(
        max_length=255,
        help_text="The venue or address where the event takes place."

    )
    start_datetime = models.DateTimeField(
        help_text="The date and time when the event starts."
    )
    end_datetime = models.DateTimeField(
        help_text='The date and time when the event ends.'
    )


    #a method to return a string representation of the event
    def __str__(self):
        return self.title