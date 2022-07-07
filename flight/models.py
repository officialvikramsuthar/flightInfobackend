from django.db import models

# Create your models here.
class Flight(models.Model):
    ticket_number = models.CharField(max_length=30)
    departure_city = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_city = models.CharField(max_length=255)
    arrival_time = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now_add=True)
