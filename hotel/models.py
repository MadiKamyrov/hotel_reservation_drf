from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Room(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat')
    number = models.CharField(max_length=50)
    floor = models.IntegerField()


class Pricing(models.Model):
    day_of_week = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ['day_of_week', 'category']


class Reservation(models.Model):
    customer_name = models.CharField(max_length=255)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
