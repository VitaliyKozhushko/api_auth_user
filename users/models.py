from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
  email = models.EmailField(unique=True)
  is_mentor = models.BooleanField()

  mentor = models.ForeignKey(
    'self',
    on_delete=models.SET_NULL,
    related_name='mentees',
    null=True,
    blank=True,
  )