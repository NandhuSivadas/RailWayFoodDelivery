from django.db import models
from django.db import models

from django.utils import timezone
from datetime import timedelta

from Guest.models import tbl_user
from Restaurant.models import tbl_food, tbl_restaurant
# Create your models here.


# class tbl_booking(models.Model):
#     user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
#     restaurant = models.ForeignKey(tbl_restaurant, on_delete=models.CASCADE)
#     food = models.ForeignKey(tbl_food, on_delete=models.CASCADE)

#     quantity = models.PositiveIntegerField()
#     delivery_time = models.TimeField()
#     booking_date = models.DateField(auto_now_add=True)

#     status = models.IntegerField(default=0)
#     # 0 = Pending
#     # 1 = Accepted
#     # 2 = Rejected

#     def __str__(self):
#         return f"{self.food.food_name} - {self.user.user_name}"


from django.db import models
from django.utils import timezone
from datetime import timedelta
from Guest.models import tbl_user, tbl_restaurant
from Restaurant.models import tbl_food


class tbl_booking(models.Model):
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(tbl_restaurant, on_delete=models.CASCADE)
    food = models.ForeignKey(tbl_food, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )  # ✅ price per item at booking time

    delivery_time = models.TimeField()
    booking_date = models.DateTimeField(auto_now_add=True)

    # 0 = Pending, 1 = Accepted, 2 = Rejected, 3 = Cancelled
    status = models.IntegerField(default=0)

    # ✅ total price calculation
    def total_amount(self):
        return self.quantity * self.price

    def can_cancel(self):
        """User can cancel only within 1 hour after booking"""
        return timezone.now() <= self.booking_date + timedelta(hours=1)

    def cancel_deadline(self):
        """Used for countdown timer"""
        return self.booking_date + timedelta(hours=1)

    def __str__(self):
        return f"{self.food.food_name} - {self.user.user_name}"
