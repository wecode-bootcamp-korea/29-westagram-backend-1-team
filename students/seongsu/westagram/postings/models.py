from django.db import models

class TimeStampModel(models.Model):
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        abstract = True

class Posting(TimeStampModel):
    post_title   = models.CharField(max_length=100)
    post_content = models.CharField(max_length=500)
    image        = models.URLField(max_length=200)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'


