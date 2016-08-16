from django.db import models

# Create your models here.
class TripMain(models.Model):
    TripName = models.CharField(max_length=255)

class Plan(models.Model):

    LocationName = models.CharField(max_length=100)
    Address = models.CharField(max_length=100,blank=True)
    Type = models.CharField(max_length=50,blank=True)
    Order = models.IntegerField(default=0)
    trip = models.ForeignKey(TripMain)
