from django.db import models

from users.models import User

class Posting(models.Model):
    content    = models.CharField(max_length=2200, null=True)
    user       = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "postings"

class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    posting   = models.ForeignKey('Posting',on_delete=models.CASCADE, related_name='images')
    
    class Meta:
        db_table = 'images'