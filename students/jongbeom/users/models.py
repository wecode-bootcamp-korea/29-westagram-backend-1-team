from django.db                     import models

class User(models.Model):
    username     = models.CharField(max_length=45)
    email        = models.EmailField(max_length=300, unique=True)
    password     = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=30, unique=True)
    
    class Meta:
        db_table = 'users'



# Create your models here.
