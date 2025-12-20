from django.db import models

# Create your models here.


class tbl_admin(models.Model):
    admin_name = models.CharField(max_length=100)
    admin_email = models.EmailField(unique=True)
    admin_password = models.CharField(max_length=100)  
    # Can be plaintext or hashed (your choice)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.admin_name
