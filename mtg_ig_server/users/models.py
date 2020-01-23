from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card1 = models.CharField(max_length=200, blank=True)
    card2 = models.CharField(max_length=200, blank=True)
    card3 = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username}"