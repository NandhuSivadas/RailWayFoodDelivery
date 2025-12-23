from django.db import models
from Guest.models import *
# Create your models here.
class tbl_food(models.Model):
    restaurant = models.ForeignKey(
        tbl_restaurant,
        on_delete=models.CASCADE,
        related_name='foods'
    )
    food_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)   # Veg / Non-Veg
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.restaurant.restaurant_name}"