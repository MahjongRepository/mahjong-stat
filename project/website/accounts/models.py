from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User


class Player(models.Model):
    user = models.ForeignKey(User, related_name='players')
    username = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_player'

    def __str__(self):
        return self.username


def user_created(sender, instance, created, **kwargs):
    if created:
        from api.models import ApiToken
        ApiToken.objects.create(user=instance)


post_save.connect(user_created, sender=User)
