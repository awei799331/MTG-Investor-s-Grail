from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    savedCards = JSONField(default={"cards":[]})

    def __str__(self):
        return f"{self.user.username}"