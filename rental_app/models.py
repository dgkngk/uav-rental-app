from django.db import models
from django.contrib.auth.models import User


class UAV(models.Model):
    brand = models.CharField(max_length=100, default="")
    model = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, default="")
    weight = models.FloatField()
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE)
    rental_start = models.DateTimeField(null=True)
    rental_end = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Rental ID: {self.id} - User: {self.user.username} - UAV: {self.uav.brand} {self.uav.model} - Active: {self.is_active}"
