from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title[:50]
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Comment(models.Model):
    article = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name = 'comments',
    )
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.comment
    
    def get_absolute_url(self):
        return reverse('post_list')
    