from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(widget=forms.PasswordInput())
    PhoneNumber = models.PhoneNumberField(unique=True, null = False, blank = False)
    class Meta:
        db_table = 'users'
