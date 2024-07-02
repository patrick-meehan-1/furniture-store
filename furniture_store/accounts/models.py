from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    age = models.PositiveBigIntegerField(null=True, blank=True)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    fav_color = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True)

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse("show_profile", args=[str(self.id)])

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()