from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
  email = models.EmailField(unique=True)
  is_mentor = models.BooleanField()

  REQUIRED_FIELDS = ['email']

  ment_user = models.ManyToManyField(
    'self',
    symmetrical=False,
    related_name='mentors',
    blank=True
  )