from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

class CustomUser(AbstractUser):
    age = models.PositiveBigIntegerField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    fav_color = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse("show_profile", args=[str(self.id)])