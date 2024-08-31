from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class User(AbstractUser):
  phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
  email = models.EmailField(unique=True, blank=True, null=True)
  is_mentor = models.BooleanField(default=False)

  mentor = models.ForeignKey(
    'self',
    on_delete=models.SET_NULL,
    related_name='mentees',
    null=True,
    blank=True,
  )

  class Meta:
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'

  def __str__(self):
    return self.username

@receiver([post_save, post_delete], sender=User)
def clear_user_cache(sender, **kwargs):
  cache.delete('views.decorators.cache.cache_page.viewset_UsersViewSet_list')