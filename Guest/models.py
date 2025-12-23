from django.db import models

# Create your models here.


class tbl_user(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    user_phone = models.CharField(max_length=15)
    user_password = models.CharField(max_length=255) 
    status = models.IntegerField(default=1)  
    # 1 = Active, 0 = Blocked
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name


from django.db import models

class tbl_restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    station_name = models.CharField(max_length=100)
    station_code = models.CharField(max_length=10)
    address = models.TextField()
    password = models.CharField(max_length=255)
    status = models.IntegerField(default=0)  
    # 0 = Pending, 1 = Approved, 2 = Rejected

    def __str__(self):
        return self.restaurant_name
