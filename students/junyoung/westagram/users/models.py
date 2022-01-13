from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField(max_lenght=100)
    phone_number = models.CharField(max_length=100)
        
    class Meta:
        db_table = 'users'    