from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField()
    phone_number = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'users'
