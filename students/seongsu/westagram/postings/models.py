from django.db import models

class Posting(models.Model):
    post_title   = models.CharField(max_length=100)
    post_content = models.CharField(max_length=500)
    image        = models.URLField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    comment      = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='userlike')
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE, related_name='postinglike')

    class Meta:
        db_table = 'likes'

class Follow(models.Model):
    follow    = models.ForeignKey('users.User', related_name='follow', on_delete=models.CASCADE)
    following = models.ForeignKey('users.User', related_name='following', on_delete=models.CASCADE)

    class Meta:
        db_table = 'follows'
